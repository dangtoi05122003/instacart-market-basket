import os
from generators.BronzeGenerator import bronze

CONFIG_PATH = os.getenv("AIRFLOW_BRONZE_PATH")

generator = bronze(path=CONFIG_PATH, layer="bronze")
generator.load_dags(globals())