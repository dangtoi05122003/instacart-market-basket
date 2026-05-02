import attr

@attr.s(auto_attribs=True, kw_only=True)
class BaseDagConfig:
    dag_id: str
    dag_type: str
    schedule_interval: str
    max_active_runs: int
    catchup: bool
    timeout_hours: int
    script_path: str
    owner: str
    retries: int
    retry_delay_min: int
    start_date: str