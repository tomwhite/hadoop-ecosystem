#!/usr/bin/env bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
BASE=$bin/..
SCRIPTS=$BASE/scripts
DATA=$BASE/data
OUTPUT=$BASE/output

mkdir -p $OUTPUT

mkdir -p $OUTPUT/raw
for project in \
  avro \
  flume \
  hadoop-common \
  hadoop-hdfs \
  hadoop-mapreduce \
  hbase \
  hcatalog \
  hive \
  hue \
  mahout \
  pig \
  sqoop \
  whirr \
  zookeeper \
  ; do
  echo $project
  $SCRIPTS/raw.py $project $DATA/repos/$project $DATA/jiras/$project.*.xml $OUTPUT/raw/$project.csv
done

echo hadoop
$SCRIPTS/raw.py hadoop $DATA/repos/hadoop $DATA/jiras/hadoop-common.*.xml $OUTPUT/raw/hadoop.csv

rm -f $OUTPUT/raw.zip
zip $OUTPUT/raw.zip $OUTPUT/raw/*