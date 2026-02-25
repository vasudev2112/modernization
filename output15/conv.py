import threading
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
import psycopg2

from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, MetadataBuilder

# Note: The Java code uses a concurrent map and thread pool executor.
# In Python, we use a thread-safe dictionary and ThreadPoolExecutor.
# The Spark code is mapped to PySpark equivalents.

class MegaUnstructuredPipeline:
    dimCache = {}
    executor = ThreadPoolExecutor(max_workers=8)

    @staticmethod
    def main(args):
        spark = SparkSession.builder \
            .appName("MegaUnstructuredPipeline") \
            .master("local[*]") \
            .config("spark.sql.shuffle.partitions", "8") \
            .getOrCreate()

        MegaUnstructuredPipeline.loadDimension()

        kafka = spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "events_topic") \
            .option("startingOffsets", "earliest") \
            .load()

        raw = kafka.selectExpr("CAST(value AS STRING)").rdd.map(lambda row: row[0])

        parsed = raw.map(lambda x: MegaUnstructuredPipeline.parse(x))

        # In PySpark, broadcast variables are created with sparkContext.broadcast
        bc = spark.sparkContext.broadcast(MegaUnstructuredPipeline.dimCache)

        def enrich(row):
            d = bc.value
            key = str(row.get("device", "NA"))
            row["device_type"] = d.get(key, "UNKNOWN")
            row["processed_ts"] = int(time.time() * 1000)
            row["random_metric"] = float(time.perf_counter()) * 1000  # Using perf_counter as a stand-in for Math.random()
            return row

        enriched = parsed.map(enrich)

        keyed = enriched.map(lambda x: (str(x.get("user", "NA")), x))

        grouped = keyed.groupByKey()

        def aggregate(tuple_):
            sum_ = 0.0
            count = 0
            maxTs = 0
            for m in tuple_[1]:
                try:
                    val = float(m.get("random_metric", "0"))
                except Exception:
                    val = 0.0
                sum_ += val
                count += 1
                try:
                    ts = int(m.get("processed_ts", "0"))
                except Exception:
                    ts = 0
                if ts > maxTs:
                    maxTs = ts
            return Row(tuple_[0], sum_, count, maxTs)

        aggregated = grouped.map(aggregate)

        schema = StructType([
            StructField("user", StringType(), False, MetadataBuilder().build()),
            StructField("metric_sum", DoubleType(), False, MetadataBuilder().build()),
            StructField("metric_count", LongType(), False, MetadataBuilder().build()),
            StructField("latest_ts", LongType(), False, MetadataBuilder().build())
        ])

        finalDf = spark.createDataFrame(aggregated, schema)

        finalDf.cache()

        def process_partition(iterator):
            batch = []
            for row in iterator:
                batch.append(row)
                if len(batch) >= 500:
                    MegaUnstructuredPipeline.writeBatch(batch)
                    batch.clear()
            if batch:
                MegaUnstructuredPipeline.writeBatch(batch)

        finalDf.foreachPartition(process_partition)

        spark.stop()
        MegaUnstructuredPipeline.executor.shutdown()

    @staticmethod
    def parse(json_str):
        map_ = {}
        try:
            cleaned = json_str.replace("{", "").replace("}", "")
            parts = cleaned.split(",")
            for p in parts:
                kv = p.split(":")
                if len(kv) == 2:
                    map_[kv[0].replace("\"", "").strip()] = kv[1].replace("\"", "").strip()
            map_["ingest_time"] = int(time.time() * 1000)
        except Exception:
            map_["error"] = "bad_record"
        return map_

    @staticmethod
    def writeBatch(rows):
        def db_task():
            conn = None
            cur = None
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    database="test",
                    user="user",
                    password="pass"
                )
                conn.autocommit = False
                cur = conn.cursor()
                sql = "insert into agg_table(user_id,metric_sum,metric_count,latest_ts) values(%s,%s,%s,%s)"
                for r in rows:
                    cur.execute(sql, (r[0], r[1], r[2], r[3]))
                conn.commit()
            except Exception:
                if conn is not None:
                    try:
                        conn.rollback()
                    except Exception:
                        pass
            finally:
                if cur is not None:
                    try:
                        cur.close()
                    except Exception:
                        pass
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass

        MegaUnstructuredPipeline.executor.submit(db_task)

    @staticmethod
    def loadDimension():
        MegaUnstructuredPipeline.dimCache.update({
            f"device{i}": "MOBILE" if i % 2 == 0 else "DESKTOP"
            for i in range(1000)
        })

if __name__ == "__main__":
    import sys
    MegaUnstructuredPipeline.main(sys.argv)
