#!/usr/bin/env bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
BASE=$bin/..

mkdir -p $BASE/data/repos
cd $BASE/data/repos

function checkout-repo() {
  repo=$1
  name=$(basename $repo .git)
  if [ -e $name ]; then
    cd $name
    git pull origin trunk
    cd -
  else
    git clone $repo
  fi
  
}

checkout-repo git://git.apache.org/avro.git
checkout-repo git://git.apache.org/flume.git
checkout-repo git://git.apache.org/hadoop-common.git
checkout-repo git://git.apache.org/hadoop-hdfs.git
checkout-repo git://git.apache.org/hadoop-mapreduce.git
checkout-repo git://git.apache.org/hbase.git
checkout-repo git://git.apache.org/hcatalog.git
checkout-repo git://git.apache.org/hive.git
# oozie
checkout-repo git://git.apache.org/mahout.git
checkout-repo git://git.apache.org/pig.git
checkout-repo git://git.apache.org/sqoop.git
checkout-repo git://git.apache.org/whirr.git
checkout-repo git://git.apache.org/zookeeper.git

checkout-repo git://github.com/cloudera/hue.git

# Checkout pre-split hadoop
if [ -e hadoop ]; then
  cd hadoop
  git pull origin pre-HADOOP-4687:pre-HADOOP-4687
  cd -
else
  git clone git://git.apache.org/hadoop-common.git hadoop
  cd hadoop
  git checkout -b pre-HADOOP-4687 origin/pre-HADOOP-4687
  cd -
fi