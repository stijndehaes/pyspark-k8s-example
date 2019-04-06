# Pyspark on kubernetes

This repository serves as an example of how you could run a pyspark app on kubernetes.

Using the spark base docker images, you can install your python code in it and then use that image to run your code.


## Requirements

- docker
- minikube (with at least 3 cpu and 4096mb ram, `minikube start --cpus 3 --memory 4096`)
- pyspark-2.4.1 or regular spark installation (install via pip, brew... , needed for spark submit)
- docker containers with spark 2.4.1 (prebuild at: sdehaes/spark:v2.4.1-hadoop-2.9.2, sdehaes/spark-py:v2.4.1-hadoop-2.9.2 )

To build the docker containers yourself you need to checkout spark at the release tag v2.4.1, the you need to use the following command to build it:

```bash
./build/mvn -Pkubernetes -DskipTests clean package -Phadoop-2.7 -Dhadoop.version=2.9.2
bin/docker-image-tool.sh -r <docker repo> -t v2.4.1 build
bin/docker-image-tool.sh -r <docker repo> -t v2.4.1 push
```

## How to run

The launch.sh script combines all necessary steps.

Add rbac roles for spark on kubernetes:

```bash
kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
```

Build the docker image:

```bash
eval $(minikube docker-env)
docker build . -t pyspark-k8s-example:2.4.1
```

In the docker image `--no-cache-dir` is used as an option for pip install. This disables [caching](https://pip.pypa.io/en/stable/reference/pip_install/#caching) making your docker image smaller.

The first command makes certain the docker image is build in the minikube environment.

Launch the spark submit:

```bash
spark-submit \
    --master k8s://https://$(minikube ip):8443 \
    --deploy-mode cluster \
    --name spark-example \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=pyspark-k8s-example:2.4.1 \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.kubernetes.pyspark.pythonVersion=3 \
    /usr/bin/run.py
```

If you get an error `Could not find valid SPARK_HOME while searching ...` then you should set spark home to the directory where pip installed pyspark.
For mac with a homebrew version of python this is:

`export SPARK_HOME=/usr/local/lib/python3.7/site-packages/pyspark`

On ubuntu this will be:

`export SPARK_HOME=//usr/local/lib/python3.7/dist-packages/pyspark`
