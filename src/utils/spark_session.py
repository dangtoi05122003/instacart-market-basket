from pyspark.sql import SparkSession
from utils.constants import JARS

def get_spark(jars: str = JARS, key:str = "/opt/spark/key.json"):
    return (
        SparkSession.builder
        .appName("Data")
        .master("local[*]")
        .config("spark.jars", jars)
        .config("spark.hadoop.google.cloud.auth.service.account.enable", "true")
        .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", key)
        .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
        .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        .getOrCreate()
    )