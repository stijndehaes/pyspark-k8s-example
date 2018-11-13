#!/usr/bin/env python

from pyspark import SparkContext, SparkConf
from pyspark_example.randomfilter import RandomFilter

if __name__ == '__main__':
    conf = SparkConf().setAppName("calculate_pyspark_example")
    sc = SparkContext(conf=conf)
    print("Random count:", RandomFilter(sc, num_samples=10000).run())
