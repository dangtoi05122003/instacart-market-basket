from src.utils import get_spark
import yaml
from pyspark.sql.functions import expr
spark = get_spark()
with open("/opt/airflow/config/gold.yaml", "r") as f:
    config = yaml.safe_load(f)
tables = config["tables"]
for name, conf in tables.items():
    dfs = {
        alias: spark.read.parquet(path).alias(alias)
        for alias, path in conf["sources"].items()
    }
    if "join" in conf:
        j = conf["join"]
        df = dfs[j["left"]].join(
            dfs[j["right"]],
            expr(j["condition"])
        )
    else:
        df = list(dfs.values())[0]
    if "group_by" in conf:
        result = df.groupBy(*conf["group_by"]).agg(
            *[expr(v).alias(k) for k, v in conf["aggregations"].items()]
        )
    else:
        result = df
    for col_name, formula in conf.get("calculated_columns", {}).items():
        result = result.withColumn(col_name, expr(formula))
    if "final_aggregations" in conf:
        result = result.agg(
            *[expr(v).alias(k) for k, v in conf["final_aggregations"].items()]
        )
    result.write.mode("overwrite").parquet(conf["output"])
