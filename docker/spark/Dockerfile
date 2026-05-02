FROM apache/spark:3.5.1

USER root
RUN apt-get update && apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*
ENV SPARK_HOME=/opt/spark
ENV PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"
WORKDIR /opt/spark
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt
RUN mkdir -p /opt/spark/src /opt/spark/data /opt/spark/config && \
    chown -R spark:spark /opt/spark/src /opt/spark/data /opt/spark/config
USER spark