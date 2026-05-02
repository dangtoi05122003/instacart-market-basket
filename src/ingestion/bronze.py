from pathlib import Path
from utils import get_spark
from utils.logger import get_logger
from utils.config_loader import load_config

logger = get_logger(__name__)
class Bronze:
    def __init__(self, path = "/opt/spark/config/bronze.yaml"):
        self.spark = get_spark()
        self.config = load_config(path)
    def run(self):
        for file in Path(self.config['path']).glob("*.csv"):
            logger.info(f"Đang đọc file: {file}")
            df = self.spark.read.csv(str(file), header=True, inferSchema=True)
            gcs_path = f"gs://{self.config['bucket']}/{self.config['gcs_prefix']}/{file.stem}"
            try:
                df.write.mode("overwrite").format("parquet").save(gcs_path)
                logger.info(f"Đẩy data hoàn tất lên gcs với bảng {file.stem}")
            except Exception as e:
                logger.error(f"Không thể đẩy data lên gcs với bảng {file.stem}: {str(e)}")
if __name__ == "__main__":
    app = Bronze()
    app.run()