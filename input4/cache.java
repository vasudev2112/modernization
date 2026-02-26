import org.apache.spark.sql.*;
import org.apache.spark.sql.types.*;
import org.apache.spark.api.java.*;
import org.apache.spark.broadcast.Broadcast;
import org.apache.spark.SparkConf;
import scala.Tuple2;

import java.sql.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class MiniChaosPipeline {

    static Map<String,String> dimCache = new ConcurrentHashMap<>();

    static Map<String,Double> metricCache =
            Collections.synchronizedMap(
                    new LinkedHashMap<String,Double>(5000,0.75f,true){
                        protected boolean removeEldestEntry(Map.Entry<String,Double> e){
                            return size()>5000;
                        }
                    });

    public static void main(String[] args) {

        SparkConf conf = new SparkConf()
                .setAppName("MiniChaosPipeline")
                .setMaster("local[*]");

        SparkSession spark = SparkSession.builder()
                .config(conf)
                .getOrCreate();

        loadDim();

        Dataset<Row> kafka = spark.read()
                .format("kafka")
                .option("kafka.bootstrap.servers","localhost:9092")
                .option("subscribe","events_topic")
                .option("startingOffsets","earliest")
                .load();

        Dataset<String> raw = kafka.selectExpr("CAST(value AS STRING)")
                .as(Encoders.STRING());

        JavaRDD<Map<String,Object>> parsed = raw.javaRDD()
                .map(x -> parse(x));

        Broadcast<Map<String,String>> bc =
                JavaSparkContext.fromSparkContext(spark.sparkContext())
                        .broadcast(dimCache);

        JavaPairRDD<String,Map<String,Object>> keyed =
                parsed.mapToPair(row -> {
                    String user = String.valueOf(row.getOrDefault("user","NA"));
                    String device = String.valueOf(row.getOrDefault("device","NA"));
                    row.put("device_type", bc.value().getOrDefault(device,"UNKNOWN"));
                    double m = Math.random()*100;
                    metricCache.put(user,m);
                    row.put("metric",m);
                    row.put("ts",System.currentTimeMillis());
                    return new Tuple2<>(user,row);
                });

        JavaPairRDD<String,Tuple2<Double,Long>> reduced =
                keyed.mapValues(v ->
                        new Tuple2<>(
                                Double.parseDouble(String.valueOf(v.get("metric"))),
                                1L))
                        .reduceByKey((a,b) ->
                                new Tuple2<>(a._1+b._1, a._2+b._2));

        JavaRDD<Row> rows = reduced.map(t -> {
            double cached = metricCache.getOrDefault(t._1,0.0);
            return RowFactory.create(
                    t._1,
                    t._2._1 + cached,
                    t._2._2,
                    System.currentTimeMillis());
        });

        StructType schema = new StructType(new StructField[]{
                new StructField("user_id",DataTypes.StringType,false,Metadata.empty()),
                new StructField("metric_sum",DataTypes.DoubleType,false,Metadata.empty()),
                new StructField("count",DataTypes.LongType,false,Metadata.empty()),
                new StructField("processed_ts",DataTypes.LongType,false,Metadata.empty())
        });

        Dataset<Row> df = spark.createDataFrame(rows, schema);

        df.cache();

        df.foreachPartition(p -> {
            Connection conn=null;
            PreparedStatement ps=null;
            try{
                conn=DriverManager.getConnection(
                        "jdbc:postgresql://localhost:5432/test",
                        "user","pass");
                ps=conn.prepareStatement(
                        "insert into agg_table(user_id,metric_sum,count,processed_ts) values(?,?,?,?)");
                while(p.hasNext()){
                    Row r=p.next();
                    ps.setString(1,r.getString(0));
                    ps.setDouble(2,r.getDouble(1));
                    ps.setLong(3,r.getLong(2));
                    ps.setLong(4,r.getLong(3));
                    ps.addBatch();
                }
                ps.executeBatch();
            }catch(Exception e){}
            finally{
                try{if(ps!=null)ps.close();}catch(Exception ex){}
                try{if(conn!=null)conn.close();}catch(Exception ex){}
            }
        });

        spark.stop();
    }

    static Map<String,Object> parse(String json){
        Map<String,Object> m=new HashMap<>();
        try{
            String[] parts=json.replace("{","").replace("}","").split(",");
            for(String p:parts){
                String[] kv=p.split(":");
                if(kv.length==2)
                    m.put(kv[0].replace("\"","").trim(),
                            kv[1].replace("\"","").trim());
            }
        }catch(Exception e){}
        return m;
    }

    static void loadDim(){
        dimCache.putAll(
                IntStream.range(0,1000)
                        .boxed()
                        .collect(Collectors.toMap(
                                i->"device"+i,
                                i->i%2==0?"MOBILE":"DESKTOP"
                        )));
    }
}
