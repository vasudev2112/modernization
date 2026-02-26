from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, Metadata
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T

import threading
import time
import random
import psycopg2

from collections import OrderedDict

class MiniChaosPipeline:
    # Equivalent to Java's static fields
    dimCache = dict()
    # Synchronized LRU cache with max size 5000
    class MetricCache(OrderedDict):
        def __init__(self, *args, **kwargs):
            self.maxsize = 5000
            self.lock = threading.Lock()
            super().__init__(*args, **kwargs)
        def __setitem__(self, key, value):
            with self.lock:
                super().__setitem__(key, value)
                if len(self) > self.maxsize:
                    self.popitem(last=False)
        def get(self, key, default=None):
            with self.lock:
                return super().get(key, default)
    metricCache = MetricCache()

    @staticmethod
    def main(args):
        conf = SparkConf().setAppName("MiniChaosPipeline").setMaster("local[*]")
        spark = SparkSession.builder.config(conf=conf).getOrCreate()

        MiniChaosPipeline.loadDim()

        kafka = spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "events_topic") \
            .option("startingOffsets", "earliest") \
            .load()

        raw = kafka.selectExpr("CAST(value AS STRING)").rdd.map(lambda row: row[0])

        parsed = raw.map(lambda x: MiniChaosPipeline.parse(x))

        sc = spark.sparkContext
        bc = sc.broadcast(MiniChaosPipeline.dimCache)

        def map_to_pair(row):
            user = str(row.get("user", "NA"))
            device = str(row.get("device", "NA"))
            row["device_type"] = bc.value.get(device, "UNKNOWN")
            m = random.random() * 100
            MiniChaosPipeline.metricCache[user] = m
            row["metric"] = m
            row["ts"] = int(time.time() * 1000)
            return (user, row)

        keyed = parsed.map(map_to_pair)

        def map_values(v):
            return (float(v.get("metric")), 1)

        def reduce_func(a, b):
            return (a[0] + b[0], a[1] + b[1])

        reduced = keyed.mapValues(map_values).reduceByKey(reduce_func)

        def make_row(t):
            user_id = t[0]
            metric_sum, count = t[1]
            cached = MiniChaosPipeline.metricCache.get(user_id, 0.0)
            return Row(
                user_id=user_id,
                metric_sum=metric_sum + cached,
                count=count,
                processed_ts=int(time.time() * 1000)
            )

        rows = reduced.map(make_row)

        schema = StructType([
            StructField("user_id", StringType(), False, Metadata()),
            StructField("metric_sum", DoubleType(), False, Metadata()),
            StructField("count", LongType(), False, Metadata()),
            StructField("processed_ts", LongType(), False, Metadata())
        ])

        df = spark.createDataFrame(rows, schema)
        df.cache()

        def foreach_partition(partition):
            conn = None
            ps = None
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    database="test",
                    user="user",
                    password="pass"
                )
                ps = conn.cursor()
                batch = []
                for r in partition:
                    batch.append((
                        r["user_id"],
                        r["metric_sum"],
                        r["count"],
                        r["processed_ts"]
                    ))
                if batch:
                    ps.executemany(
                        "insert into agg_table(user_id,metric_sum,count,processed_ts) values(%s,%s,%s,%s)",
                        batch
                    )
                    conn.commit()
            except Exception:
                pass
            finally:
                try:
                    if ps is not None:
                        ps.close()
                except Exception:
                    pass
                try:
                    if conn is not None:
                        conn.close()
                except Exception:
                    pass

        df.rdd.foreachPartition(foreach_partition)

        spark.stop()

    @staticmethod
    def parse(json_str):
        m = dict()
        try:
            parts = json_str.replace("{", "").replace("}", "").split(",")
            for p in parts:
                kv = p.split(":")
                if len(kv) == 2:
                    k = kv[0].replace("\"", "").strip()
                    v = kv[1].replace("\"", "").strip()
                    m[k] = v
        except Exception:
            pass
        return m

    @staticmethod
    def loadDim():
        MiniChaosPipeline.dimCache.update({
            f"device{i}": "MOBILE" if i % 2 == 0 else "DESKTOP"
            for i in range(1000)
        })

if __name__ == "__main__":
    import sys
    MiniChaosPipeline.main(sys.argv)
