import yaml
from utils.logger import get_logger

logger = get_logger(__name__)
def load_config(path):
    try:
        with open(path, "r") as f:
            config =  yaml.safe_load(f)
            logger.info("Tải file cấu hình thành công.")
            return config
    except Exception as e:
        logger.error(f"Lỗi khi tải file cấu hình tại {path}: {e}")
        raise