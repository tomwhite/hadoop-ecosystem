#!/usr/bin/env bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
BASE=$bin/..

mkdir -p $BASE/data/repos
cd $BASE/data/repos

function checkout-repo() {
  repo=$1
  if [ -e $repo ]; then
    cd $repo
    git pull origin trunk
    cd -
  else
    git clone git://git.apache.org/$repo.git
  fi
}

checkout-repo avro
checkout-repo flume
checkout-repo hadoop-hdfs
checkout-repo hadoop-mapreduce
checkout-repo hbase
checkout-repo hive
# oozie
checkout-repo pig
checkout-repo sqoop
checkout-repo whirr
checkout-repo zookeeper