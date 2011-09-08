#!/usr/bin/env bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
BASE=$bin/..
SCRIPTS=$BASE/scripts
DATA=$BASE/data
OUTPUT=$BASE/output

mkdir -p $OUTPUT

mkdir -p $OUTPUT/raw
for project in avro; do
  $SCRIPTS/raw.py $project $DATA/repos/$project $DATA/jiras/$project.*.xml $OUTPUT/raw/$project.tsv
done
