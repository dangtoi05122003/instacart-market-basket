from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from generators.base import BaseGenerator
from models.base import BaseDagConfig
from utils.constants import JARS

class Generator(BaseGenerator):
    def __init__(self, path, layer: str):
        super().__init__(path)
        self.layer = layer
    def load_dags(self, global_session):
        for path in self.load_config_path():
            data = (self.load_file(path)).get("general", {})
            defaults = data.get('default_settings', {})
            for config_item in data.get('dag_configs', []):
                conf = BaseDagConfig(**{**defaults, **config_item})
                global_session[conf.dag_id] = self.create_airflow_dag(conf)
    def get_bash_command(self, conf):
        return f"docker exec spark spark-submit --master local[*] --jars {JARS} {conf.script_path}"
    def create_airflow_dag(self, conf):
        dag = DAG(
            dag_id=conf.dag_id,
            default_args={
                'owner': conf.owner,
                'retries': conf.retries,
                'retry_delay': timedelta(minutes=conf.retry_delay_min),
            },
            schedule_interval=conf.schedule_interval,
            start_date=datetime.strptime(conf.start_date, '%Y-%m-%d'),
            catchup=conf.catchup,
            max_active_runs=conf.max_active_runs,
            is_paused_upon_creation=False,
            tags=[self.layer, conf.dag_type]
        )
        with dag:
            BashOperator(
                task_id='instacart',
                bash_command=self.get_bash_command(conf),
                execution_timeout=timedelta(hours=conf.timeout_hours)
            )
        return dag