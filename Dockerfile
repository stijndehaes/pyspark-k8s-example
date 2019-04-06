FROM sdehaes/spark-py:v2.4.1-hadoop-2.9.2

COPY . /app
WORKDIR /app
RUN python3 -m pip install . --no-cache-dir
