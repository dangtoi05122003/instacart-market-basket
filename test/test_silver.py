from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def test_no_null_order_id(spark):
    df = spark.read.parquet(str(BASE_DIR / "data/silver/orders"))
    assert df.filter("order_id is null").count() == 0

def test_products_row_count(spark):
    bronze = spark.read.parquet(str(BASE_DIR / "data/bronze/products"))
    silver = spark.read.parquet(str(BASE_DIR / "data/silver/products"))
    assert bronze.count() == silver.count()

def test_fillna_orders(spark):
    df = spark.read.parquet(str(BASE_DIR / "data/silver/orders"))
    assert df.filter("days_since_prior_order is null").count() == 0