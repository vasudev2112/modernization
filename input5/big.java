import org.apache.spark.sql.*;
import org.apache.spark.sql.types.*;
import org.apache.spark.api.java.function.*;
import org.apache.spark.api.java.*;
import org.apache.spark.broadcast.Broadcast;
import org.apache.spark.SparkConf;
import scala.Tuple2;

import java.sql.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;
import java.time.*;
import java.time.format.*;

public class MegaUnstructuredPipeline {

    static Map<String,String> dimCache = new ConcurrentHashMap<>();
    static ExecutorService executor = Executors.newFixedThreadPool(8);

    public static void main(String[] args) throws Exception {

        SparkConf conf = new SparkConf()
                .setAppName("MegaUnstructuredPipeline")
                .setMaster("local[*]")
                .set("spark.sql.shuffle.partitions","8");

        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        loadDimension();

        Dataset<Row> kafka = spark.read()
                .format("kafka")
                .option("kafka.bootstrap.servers","localhost:9092")
                .option("subscribe","events_topic")
                .option("startingOffsets","earliest")
                .load();

        Dataset<String> raw = kafka.selectExpr("CAST(value AS STRING)")
                .as(Encoders.STRING());

        JavaRDD<String> rdd = raw.javaRDD();

        JavaRDD<Map<String,Object>> parsed = rdd.map(x -> parse(x));

        Broadcast<Map<String,String>> bc = JavaSparkContext.fromSparkContext(spark.sparkContext()).broadcast(dimCache);

        JavaRDD<Map<String,Object>> enriched = parsed.map(row -> {
            Map<String,String> d = bc.value();
            String key = String.valueOf(row.getOrDefault("device","NA"));
            row.put("device_type", d.getOrDefault(key,"UNKNOWN"));
            row.put("processed_ts", System.currentTimeMillis());
            row.put("random_metric", Math.random()*1000);
            return row;
        });

        JavaPairRDD<String,Map<String,Object>> keyed = enriched.mapToPair(x -> 
                new Tuple2<>(String.valueOf(x.getOrDefault("user","NA")), x)
        );

        JavaPairRDD<String,Iterable<Map<String,Object>>> grouped =
                keyed.groupByKey();

        JavaRDD<Row> aggregated = grouped.map(tuple -> {
            double sum = 0;
            long count = 0;
            long maxTs = 0;
            for(Map<String,Object> m : tuple._2){
                double val = Double.parseDouble(String.valueOf(m.getOrDefault("random_metric","0")));
                sum += val;
                count++;
                long ts = Long.parseLong(String.valueOf(m.getOrDefault("processed_ts","0")));
                if(ts>maxTs) maxTs=ts;
            }
            return RowFactory.create(tuple._1,sum,count,maxTs);
        });

        StructType schema = new StructType(new StructField[]{
                new StructField("user",DataTypes.StringType,false,Metadata.empty()),
                new StructField("metric_sum",DataTypes.DoubleType,false,Metadata.empty()),
                new StructField("metric_count",DataTypes.LongType,false,Metadata.empty()),
                new StructField("latest_ts",DataTypes.LongType,false,Metadata.empty())
        });

        Dataset<Row> finalDf = spark.createDataFrame(aggregated, schema);

        finalDf.cache();

        finalDf.foreachPartition(partition -> {
            List<Row> batch = new ArrayList<>();
            while(partition.hasNext()){
                batch.add(partition.next());
                if(batch.size()>=500){
                    writeBatch(batch);
                    batch.clear();
                }
            }
            if(!batch.isEmpty()) writeBatch(batch);
        });

        spark.stop();
        executor.shutdown();
    }

    static Map<String,Object> parse(String json){
        Map<String,Object> map = new HashMap<>();
        try{
            String cleaned = json.replace("{","").replace("}","");
            String[] parts = cleaned.split(",");
            for(String p : parts){
                String[] kv = p.split(":");
                if(kv.length==2){
                    map.put(kv[0].replace("\"","").trim(),
                            kv[1].replace("\"","").trim());
                }
            }
            map.put("ingest_time", Instant.now().toEpochMilli());
        }catch(Exception e){
            map.put("error","bad_record");
        }
        return map;
    }

    static void writeBatch(List<Row> rows){
        executor.submit(() -> {
            Connection conn=null;
            PreparedStatement ps=null;
            try{
                conn=DriverManager.getConnection(
                        "jdbc:postgresql://localhost:5432/test",
                        "user","pass");
                conn.setAutoCommit(false);
                ps=conn.prepareStatement(
                        "insert into agg_table(user_id,metric_sum,metric_count,latest_ts) values(?,?,?,?)");
                for(Row r:rows){
                    ps.setString(1,r.getString(0));
                    ps.setDouble(2,r.getDouble(1));
                    ps.setLong(3,r.getLong(2));
                    ps.setLong(4,r.getLong(3));
                    ps.addBatch();
                }
                ps.executeBatch();
                conn.commit();
            }catch(Exception ex){
                try{ if(conn!=null) conn.rollback(); }catch(Exception ignore){}
            }finally{
                try{ if(ps!=null) ps.close(); }catch(Exception ignore){}
                try{ if(conn!=null) conn.close(); }catch(Exception ignore){}
            }
        });
    }

    static void loadDimension(){
        dimCache.putAll(
                IntStream.range(0,1000)
                        .boxed()
                        .collect(Collectors.toMap(
                                i -> "device"+i,
                                i -> i%2==0?"MOBILE":"DESKTOP"
                        ))
        );
    }
}
