FROM sdehaes/spark-py:v2.4.0

# Cache this layer
RUN python3 -m pip install pyspark==2.4.0

COPY . /app
WORKDIR /app
RUN python3 -m pip install .
