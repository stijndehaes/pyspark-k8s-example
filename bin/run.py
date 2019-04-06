#!/usr/bin/env python

from pyspark import SparkContext, SparkConf
from pyspark_example.randomfilter import RandomFilter

if __name__ == '__main__':
    conf = SparkConf().setAppName("calculate_pyspark_example")
    with SparkContext(conf=conf) as sc:
        print("Random count:", RandomFilter(sc, num_samples=100000).run())
