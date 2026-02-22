from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))
import pytest
from src.utils import get_spark

@pytest.fixture(scope="session")
def spark():
    spark = get_spark()
    yield spark
    spark.stop()