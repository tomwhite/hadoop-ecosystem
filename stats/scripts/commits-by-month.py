#!/usr/bin/env python

import collections
import operator
import subprocess
import sys

from util import generate_monthly_activity_page

args = sys.argv[1:]

project=args[0]
repo=args[1]

# Find author and date of all commits
p = subprocess.Popen('git log --format="%ae %ad" --date=short', shell=True, cwd=repo, stdout=subprocess.PIPE)
output, errors = p.communicate()

# Parse records
records=[]
for line in output.split("\n"):
  fields = line.split(" ")
  if (len(fields) == 2):
    committer, month = fields[0].split("@")[0], fields[1][:-3]
    records.append((committer,month))
    
print generate_monthly_activity_page(project, records)
