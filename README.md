# Pyspark on kubernetes

This repository serves as an example of how you could run a pyspark app on kubernetes.

Using the spark base docker images, you can install your python code in it and then use that image to run your code.


## Requirements

- docker
- minikube


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
    --master k8s://https://192.168.99.100:8443 \
    --deploy-mode cluster \
    --name spark-example \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=pyspark-k8s-example:2.4.0 \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    /usr/bin/run.py
```