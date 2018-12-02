# Pyspark on kubernetes

This repository serves as an example of how you could run a pyspark app on kubernetes.

Using the spark base docker images, you can install your python code in it and then use that image to run your code.


## Requirements

- docker
- minikube (with at least 3 cpu and 4096mb ram, `minikube start --cpus 3 --memory 4096`)
- pyspark-2.4.0 (install via pip, needed for spark submit)
- docker containers with spark 2.4.0 (prebuild at: sdehaes/spark:v2.4.0, sdehaes/spark-py:v2.4.0)

To build the docker containers yourself you need to checkout spark at the release tag v2.4.0, the you need to use the following command to build it:

```bash
./build/mvn -Pkubernetes -DskipTests clean package
bin/docker-image-tool.sh -r <docker repo> -t v2.4.0 build
bin/docker-image-tool.sh -r <docker repo> -t v2.4.0 push
```

## How to run

the launch.sh script combines all necessary steps.

Add rbac roles for spark on kubernetes:

```bash
kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
```

Build the docker image:

```bash
eval $(minikube docker-env)
docker build . -t pyspark-k8s-example:2.4.0
```
The first command makes certain the docker image is build in the minikube environment.

Launch the spark submit:

```bash
spark-submit \
    --master k8s://https://$(minikube ip):8443 \
    --deploy-mode cluster \
    --name spark-example \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=pyspark-k8s-example:2.4.0 \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.kubernetes.pyspark.pythonVersion=3 \
    /usr/bin/run.py
```

If you get an error `Could not find valid SPARK_HOME while searching ...` then you should set spark home to the directory where pip installed pyspark.
For mac with a homebrew version of python this is:

`export SPARK_HOME=/usr/local/lib/python3.7/site-packages/pyspark`

On ubuntu this will be:

`export SPARK_HOME=//usr/local/lib/python3.7/dist-packages/pyspark`
