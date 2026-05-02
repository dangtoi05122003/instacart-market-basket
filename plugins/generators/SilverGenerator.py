from generators.DagGenerator import Generator

class silver(Generator):
    def __init__(self, path, layer):
        super().__init__(path, layer)
    def get_bash_command(self, conf):
        return f"cd /opt/airflow/instacart && {conf.script_path} --profiles-dir /opt/airflow"