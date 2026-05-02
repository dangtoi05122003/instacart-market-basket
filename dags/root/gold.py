import os
from generators.GoldGenerator import gold

CONFIG_PATH = os.getenv("AIRFLOW_GOLD_PATH")

generator = gold(path=CONFIG_PATH, layer="gold")
generator.load_dags(globals())