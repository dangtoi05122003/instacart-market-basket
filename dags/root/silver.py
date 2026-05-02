import os
from generators.SilverGenerator import silver

CONFIG_PATH = os.getenv("AIRFLOW_SILVER_PATH")

generator = silver(path=CONFIG_PATH, layer="silver")
generator.load_dags(globals())