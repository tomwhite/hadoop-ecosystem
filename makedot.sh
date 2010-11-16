#!/bin/bash
for file in *.dot; do
  dot -Tpng $file -O
done