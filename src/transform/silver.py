from pathlib import Path
import sys
import yaml
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))
from src.utils import get_spark
from functools import reduce
config_path = BASE_DIR / "config" / "silver.yaml"
input_path =  BASE_DIR / "data" / "bronze"
output_path =  BASE_DIR / "data" / "silver"
def load_config():
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
spark = get_spark()
def run(table_name):
    config = load_config()["tables"][table_name]
    combine_type = config["combine"]
    if combine_type == "single":
        df = spark.read.parquet(str(input_path / config["inputs"][0]))
    elif combine_type == "union":
        dfs = [
            spark.read.parquet(str(input_path / file))
            for file in config["inputs"]
        ]
        df = reduce(lambda a, b: a.unionByName(b), dfs)
    elif combine_type == "join":
        tables = {
            name: spark.read.parquet(str(input_path / file))
            for name, file in config["inputs"].items()
        }
        df = tables[config["joins"][0]["left"]]
        for j in config["joins"]:
            df = df.join(tables[j["right"]], on=j["join_on"], how=j["how"])
    if "fillna" in config:
        df = df.fillna(config["fillna"])
    df.write.mode("overwrite").parquet(str(output_path / config["output"]))
if __name__ == "__main__":
    table = sys.argv[1]
    run(table)