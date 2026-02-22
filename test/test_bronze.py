from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
raw_path = BASE_DIR / "data" / "raw"
bronze_path = BASE_DIR / "data" / "bronze"
def test_row_count(spark):
    for file in raw_path.glob("*.csv"):
        df = spark.read.csv(str(file),header=True, inferSchema=True)
        parquet_bronze = spark.read.parquet(str(bronze_path / file.stem))
        assert df.count() == parquet_bronze.count(), f"Data length mismatch in {file.stem}"