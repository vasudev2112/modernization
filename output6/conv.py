import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.functions import col, lit, to_timestamp, when
from pyspark.sql.utils import AnalysisException

class UserMetricsJob:

    @staticmethod
    def get_arg(args, key, default):
        # Placeholder: actual implementation not visible in Java code
        for i, arg in enumerate(args):
            if arg == key and i + 1 < len(args):
                return args[i + 1]
        return default

    @staticmethod
    def main(args):
        events_path = UserMetricsJob.get_arg(args, "--events", "sample_data/events.csv")
        users_path  = UserMetricsJob.get_arg(args, "--users",  "sample_data/users.csv")
        out_path    = UserMetricsJob.get_arg(args, "--out",    "out/user_metrics_parquet")
        min_date    = UserMetricsJob.get_arg(args, "--from",   "1970-01-01")
        max_date    = UserMetricsJob.get_arg(args, "--to",     "2100-01-01")
        use_udf     = UserMetricsJob.get_arg(args, "--useUdf", "false").lower() == "true"

        spark = SparkSession.builder \
            .appName("UserMetricsJob") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.shuffle.partitions", "8") \
            .getOrCreate()

        try:
            # Logging omitted as per anti-hallucination rules

            events = UserMetricsJob.load_events(spark, events_path)
            users  = UserMetricsJob.load_users(spark, users_path)

            transformed = UserMetricsJob.transform(events, users, min_date, max_date, use_udf)

            transformed \
                .coalesce(1) \
                .write \
                .mode("overwrite") \
                .format("parquet") \
                .save(out_path)

            transformed.show(truncate=False)

            # Logging omitted as per anti-hallucination rules
        except AnalysisException as ae:
            # Logging omitted as per anti-hallucination rules
            raise RuntimeError("Analysis exception during job run") from ae
        except Exception as e:
            # Logging omitted as per anti-hallucination rules
            raise RuntimeError("Unhandled exception") from e
        finally:
            spark.stop()

    @staticmethod
    def load_events(spark, path):
        schema = StructType([
            StructField("user_id", StringType(), True),
            StructField("event_type", StringType(), True),
            StructField("score", IntegerType(), True),
            StructField("amount", DoubleType(), True),
            StructField("ts", TimestampType(), True)
        ])

        return spark.read \
            .option("header", "true") \
            .schema(schema) \
            .csv(path)

    @staticmethod
    def load_users(spark, path):
        schema = StructType([
            StructField("user_id", StringType(), False),
            StructField("country", StringType(), True)
        ])

        return spark.read \
            .option("header", "true") \
            .schema(schema) \
            .csv(path)

    @staticmethod
    def transform(events, users, min_date_inclusive, max_date_exclusive, use_udf_bucket):
        in_window = (
            col("ts") >= to_timestamp(lit(min_date_inclusive))
        ) & (
            col("ts") < to_timestamp(lit(max_date_exclusive))
        )

        filtered = events \
            .filter(col("event_type").isin(["click", "purchase"])) \
            .filter(in_window)

        if use_udf_bucket:
            # Placeholder for sparkRegisterBucketUdf: actual implementation not visible in Java code
            filtered = filtered.withColumn("score_bucket", UserMetricsJob.call_udf_bucket_score(filtered.sparkSession, col("score")))
        else:
            filtered = filtered.withColumn(
                "score_bucket",
                when(col("score").isNull(), lit("unknown"))
                .when(col("score") >= lit(80), lit("high"))
                # The rest of the logic is not present in the provided Java code snippet
            )
        return filtered

    @staticmethod
    def call_udf_bucket_score(spark_session, score_col):
        # Placeholder for callUDF("bucketScore", col("score"))
        # Actual UDF registration and usage not shown in Java code
        return score_col

if __name__ == "__main__":
    UserMetricsJob.main(sys.argv[1:])
