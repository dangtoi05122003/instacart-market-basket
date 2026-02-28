import sys
from pathlib import Path
sys.path.append("/opt/airflow")
import yaml
from src.utils import get_spark
from functools import reduce
from google.cloud import storage
with open("/opt/airflow/config/silver.yaml", "r") as f:
    config = yaml.safe_load(f)
spark = get_spark()
client = storage.Client()
bucket = client.bucket(config["bucket"])
gcs_prefix = config["gcs_prefix"]
def upload_to_gcs(local_folder: Path, table_name: str):
    gcs_folder = f"{gcs_prefix}/{table_name}/"
    blobs = bucket.list_blobs(prefix=gcs_folder)
    for blob in blobs:
        blob.delete()
    for file in local_folder.rglob("*.parquet"):
        object_name = f"{gcs_folder}{file.name}"
        blob = bucket.blob(object_name)
        blob.upload_from_filename(str(file))
    print(f"Uploaded to gs://{bucket.name}/{gcs_folder}")
def run():
    table = config["tables"]
    for table_name, table_config in table.items():
        print(f"Processing: {table_name}")
        combine_type = table_config["combine"]
        if combine_type == "single":
            df = spark.read.parquet(str(table_config["inputs"][0]))
        elif combine_type == "union":
            dfs = [
                spark.read.parquet(str(file))
                for file in table_config["inputs"]
            ]
            df = reduce(lambda a, b: a.unionByName(b), dfs)
        elif combine_type == "join":
            tables = {
                name: spark.read.parquet(str(file))
                for name, file in table_config["inputs"].items()
            }
            df = tables[table_config["joins"][0]["left"]]
            for j in table_config["joins"]:
                df = df.join(tables[j["right"]], on=j["join_on"], how=j["how"])
        if "fillna" in table_config:
            df = df.fillna(table_config["fillna"])
        local_output = Path(table_config["output"])
        print("Local output path:", local_output)
        print("Files:", list(local_output.rglob("*.parquet")))
        df.write.mode("overwrite").parquet(str(local_output))
        upload_to_gcs(local_output, local_output.name)
if __name__ == "__main__":
    run()