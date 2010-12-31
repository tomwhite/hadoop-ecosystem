#!/usr/bin/env python

from xml.etree import ElementTree as ET
from email.utils import parsedate_tz
import re
import sys
import urllib

from util import generate_monthly_activity_page

args = sys.argv[1:]

project=args[0]
threshold=int(args[1])
files=args[2:]

class ElementWrapper:
  def __init__(self, element):
    self._element = element
  def __getattr__(self, tag):
    if tag.startswith("__"):
      raise AttributeError(tag)
    return self._element.findtext(tag)

def get_contributions(project, files):
  contributions = []
  for file in files:
    doc = ET.parse(file)
    for item in doc.findall("channel/item"):
      resolution_date = ElementWrapper(item).updated
      for field in item.findall("customfields/customfield"):
        if field.attrib["key"] == "com.atlassian.jira.ext.charting:resolutiondate":
          resolution_date = field.findtext("customfieldvalues/customfieldvalue")
      contributions.append((parsedate_tz(resolution_date), ElementWrapper(item).assignee))
  return contributions

records = [(contributor, "%d-%02d" % (dt[0], dt[1])) for (dt, contributor) in get_contributions(project, files)]

print generate_monthly_activity_page(project, records, threshold)