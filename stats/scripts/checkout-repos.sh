#!/usr/bin/env bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
BASE=$bin/..

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
checkout-repo hadoop-hdfs
checkout-repo hadoop-mapreduce
checkout-repo pig
checkout-repo hbase
checkout-repo hive
checkout-repo whirr
checkout-repo zookeeper