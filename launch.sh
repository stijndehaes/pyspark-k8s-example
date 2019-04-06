#!/usr/bin/env bash
set -e

if ! kubectl get serviceaccount spark; then
    kubectl create serviceaccount spark
    kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
fi

eval $(minikube docker-env)
docker build . -t pyspark-k8s-example:2.4.1

spark-submit \
    --master k8s://https://$(minikube ip):8443 \
    --deploy-mode cluster \
    --name spark-example \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.container.image=pyspark-k8s-example:2.4.1 \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.kubernetes.pyspark.pythonVersion=3 \
    /usr/bin/run.py
