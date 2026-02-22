from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))
from src.utils import get_spark
spark = get_spark()
raw_path = BASE_DIR / "data" / "raw"
out_path = BASE_DIR / "data" / "bronze"
for file in raw_path.glob("*.csv"):
    df = spark.read.csv(str(file), header=True, inferSchema=True)
    output = out_path / file.stem
    df.write.mode("overwrite").parquet(str(output))
    print(f"Converted {file.name} → {file.stem}.parquet")
