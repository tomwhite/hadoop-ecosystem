import collections
import operator

# TODO: Do total commits at the top row (need to adjust max)
def generate_monthly_activity_page(project, records, threshold=0):
  """Generate an HTML page of activity sparklines by month for people.
records is a list of (person, month) tuples, where month is a string of the form "YYYY-MM"."""

  # Aggregate by committer and month
  committer_month_counts = collections.defaultdict(int)
  for committer, month in records:
    committer_month_counts[committer, month] += 1

  # Find high water mark
  max_commits_per_month = max(committer_month_counts.iteritems(), key=operator.itemgetter(1))[1]

  # Find committers totals
  committer_total_counts = collections.defaultdict(int)
  for committer, _ in records:
    committer_total_counts[committer] += 1
    
  # Filter those at or below threshold
  committer_total_counts = dict((k, v) for k, v in committer_total_counts.iteritems() if v > threshold)

  # Find all months
  # TODO - need to find earliest month to cope with case when no commits were made....
  months = sorted(set(m for (c,m) in committer_month_counts.iterkeys()))

  header = "<th>Committer</th><th>Commits (%s to %s)</th>" % (months[0], months[-1])

  rows=[]
  # Sort by most prolific committer
  s = sorted(committer_total_counts.iteritems(), key=operator.itemgetter(1), reverse=True)
  for committer, _ in s:
    counts = []
    for month in months:
      counts.append(str(committer_month_counts[(committer,month)]))
    rows.append(u'<tr><td>%s</td><td><img src="http://sparklines.bitworking.info/spark.cgi?type=impulse&d=%s&height=40&limits=0,%s&upper=1&above-color=red&below-color=gray&width=8"></td></tr>\n' % (committer, ",".join(counts), max_commits_per_month))

  return """
<html>
<head>
  <title>%s commits per month by committer</title>
</head>
<body>

<table cellpadding="2" cellspacing="2">
<thead>
%s
</thead>
<tbody>
%s
</tbody>
</table>
</body>
</html>
""" % (project.title(), header, "".join(rows))

