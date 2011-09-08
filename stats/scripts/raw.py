#!/usr/bin/env python

from xml.etree import ElementTree as ET
from email.utils import parsedate_tz
import codecs
import re
import sys
import urllib

import collections
import operator
import subprocess

args = sys.argv[1:]

project=args[0]
repo=args[1]
files=args[2:-1]
out=args[-1]

def build_jira_to_assignee_dict():
  d = {}
  for file in files:
    doc = ET.parse(file)
    for item in doc.findall("channel/item"):
      d[ElementWrapper(item).key] = unicode(ElementWrapper(item).assignee)
  return d
  
def parse_jira(message):
  jira_match = re.match("%s-[0-9]+" % project.upper(), message.lstrip())
  if jira_match:
    jira = jira_match.group(0)
  else:
    jira = ""
  return jira
  
def parse_contributors(message):
  contributors_match = re.search("Contributed by (.*)", message)
  c = []
  if contributors_match:
    contributors = contributors_match.group(1)
    contributors = contributors.replace("&", ",")
    contributors = re.sub(r'\band\b', ',', contributors)
    c = contributors.split(",")
    c = [(safe_unicode(contributor.strip().rstrip('.)'))) for contributor in c]
  return c
  
def find_change_summary(hash):
  p = subprocess.Popen('git show --shortstat %s' % hash, shell=True, cwd=repo, stdout=subprocess.PIPE)
  output, errors = p.communicate()
  match = re.search('(\d+) insertions\(\+\), (\d+) deletions\(-\)', output)
  if match == None:
    return ("0", "0")
  return match.group(1), match.group(2)

def get_commits():
  # Find author and date of all commits
  p = subprocess.Popen('git log --format="%H\t%ae\t%ad\t%s" --date=short', shell=True, cwd=repo, stdout=subprocess.PIPE)
  output, errors = p.communicate()

  jira_to_assignee=build_jira_to_assignee_dict()
  # Parse records
  records=[]
  for line in output.split("\n"):
    fields = line.split("\t")
    if (len(fields) != 4):
      continue
    hash, committer, date, message = fields
    jira = parse_jira(message)
    contributors = ",".join(parse_contributors(message))
    assignee = jira_to_assignee.get(jira, u'')
    insertions, deletions = find_change_summary(hash)
    records.append((hash, committer, date, jira, contributors, assignee, insertions, deletions, message))
  return records

class ElementWrapper:
  def __init__(self, element):
    self._element = element
  def __getattr__(self, tag):
    if tag.startswith("__"):
      raise AttributeError(tag)
    return self._element.findtext(tag)

def safe_unicode(obj, *args):
  """ return the unicode representation of obj """
  try:
    return unicode(obj, *args)
  except UnicodeDecodeError:
    # obj is byte string
    ascii_text = str(obj).encode('string_escape')
    return unicode(ascii_text)
    
# Following is convoluted due to UTF-8 problems - it could likely be simplified
f = codecs.open(out,'w','utf-8')
f.write("Commit hash\tCommitter email\tDate\tJira\tContributors\tAssignee\tInsertions\tDeletions\tCommit message\n")
for c in get_commits():
    for t in c:
      if type(t) == str:
        f.write(safe_unicode(t))
      else:
        f.write(t)
      f.write("\t")
    f.write("\n") 
f.close()
