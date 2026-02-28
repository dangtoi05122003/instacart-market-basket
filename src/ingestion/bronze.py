from pathlib import Path
import sys
sys.path.append("/opt/airflow")
from src.utils import get_spark
from google.cloud import storage
spark = get_spark()
raw_path = Path("/opt/airflow/data/raw")
out_path = Path("/opt/airflow/data/bronze")
client = storage.Client()
bucket = client.bucket("instacart-platform")
for file in raw_path.glob("*.csv"):
    df = spark.read.csv(str(file), header=True, inferSchema=True)
    output = out_path / file.stem
    df.write.mode("overwrite").parquet(str(output))
    print(f"Converted {file.name} → {file.stem}.parquet")
    for parquet_file in output.rglob("*.parquet"):
        object_name = f"bronze/{file.stem}/{parquet_file.name}"
        blob = bucket.blob(object_name)
        blob.upload_from_filename(str(parquet_file))