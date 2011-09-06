#!/usr/bin/env bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
BASE=$bin/..
SCRIPTS=$BASE/scripts
DATA=$BASE/data
OUTPUT=$BASE/output

mkdir -p $OUTPUT
cp $bin/index.html $OUTPUT

mkdir -p $OUTPUT/committer-commits-by-month/
for project in avro hadoop-hdfs hadoop-mapreduce hbase hive pig whirr zookeeper; do
  $SCRIPTS/commits-by-month.py $project $DATA/repos/$project \
    > $OUTPUT/committer-commits-by-month/$project.html
done

mkdir -p $OUTPUT/contributions-by-month/
for project in avro flume hadoop-common hadoop-mapreduce hive pig sqoop whirr zookeeper; do
  $SCRIPTS/contributions-by-month.py $project 1 $DATA/jiras/$project.*.xml \
    > $OUTPUT/contributions-by-month/$project.html
done

mkdir -p $OUTPUT/releases/
for project in hadoop pig; do
  $SCRIPTS/release-dates.py $project $DATA/releases.txt \
    > $OUTPUT/releases/$project.html
done