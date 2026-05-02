FROM apache/airflow:2.8.3-python3.9
USER root
RUN apt-get update && apt-get clean 
USER airflow
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt