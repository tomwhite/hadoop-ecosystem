#!/usr/bin/env python

from xml.etree import ElementTree as ET
import os
import sys
import urllib

JIRA_DIR = os.path.join(sys.path[0], "../data/jiras")
APACHE_JIRA_URL='https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?pid=%s&resolution=1&sorter/field=issuekey&sorter/order=DESC&tempMax=%s&pager/start=%s'
CLOUDERA_JIRA_URL='https://issues.cloudera.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?pid=%s&resolution=1&sorter/field=issuekey&sorter/order=DESC&tempMax=%s&pager/start=%s'

if not os.path.exists(JIRA_DIR):
  os.makedirs(JIRA_DIR)

def get_fixed_jiras_url(project_id, url, start=0, page_size=1000):
  return url % (project_id, page_size, start)
    
def retrieve_jiras(project, project_id, url=APACHE_JIRA_URL, page=1):
  start = 0
  while True:
    filename = os.path.join(JIRA_DIR, "%s.%s.xml" % (project, page))
    print "Downloading %s ..." % filename
    urllib.urlretrieve(get_fixed_jiras_url(project_id, url, start), filename)
    doc = ET.parse(filename)
    end = int(doc.find("channel/issue").attrib["end"])
    total = int(doc.find("channel/issue").attrib["total"])
    if total == end:
      break
    else:
      page = page + 1
      start = end + 1

# Find project IDs from https://issues.apache.org/jira/secure/BrowseProjects.jspa

retrieve_jiras("avro", "12310911")
retrieve_jiras("flume", "12311321")
retrieve_jiras("hadoop-common", "12310240")
retrieve_jiras("hadoop-hdfs", "12310942")
retrieve_jiras("hadoop-mapreduce", "12310941")
retrieve_jiras("hbase", "12310753")
retrieve_jiras("hcatalog", "12311291")
retrieve_jiras("hive", "12310843")
retrieve_jiras("mahout", "12310751")
# oozie
retrieve_jiras("pig", "12310730")
retrieve_jiras("sqoop", "10000", CLOUDERA_JIRA_URL) # old issues on Cloudera JIRA
retrieve_jiras("sqoop", "12311320", APACHE_JIRA_URL, 2)
retrieve_jiras("whirr", "12311110")
retrieve_jiras("zookeeper", "12310801")

retrieve_jiras("hue", "10011", CLOUDERA_JIRA_URL)
