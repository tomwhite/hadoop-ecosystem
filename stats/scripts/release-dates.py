#!/usr/bin/env python

import collections
from collections import defaultdict
from datetime import datetime
import operator
import subprocess
import sys

args = sys.argv[1:]

project=args[0]
releases_filename=args[1]

releases_file = open(releases_filename)

minor_versions = defaultdict(list)
for line in releases_file.readlines():
  p, date, version = line.strip().split('\t')
  if project == p.lower():
    dt = datetime.strptime(date, "%Y-%m-%d")
    minor_version = ".".join(version.split(".")[0:2])
    minor_versions[minor_version].append((dt.strftime("%b %d, %Y"), version))
releases_file.close()

z = []
for k, v in minor_versions.items():
  x = []
  for vs in v:
    x.append('[dt("%s", "%s"), %s]' % (vs[0], vs[1], k))
  z.append("[%s]" % ", ".join(x))

print """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<html> 
 <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
    <title>%s Releases</title> 
    <link href="layout.css" rel="stylesheet" type="text/css"></link> 
    <!--[if IE]><script language="javascript" type="text/javascript" src="flot/excanvas.min.js"></script><![endif]--> 
    <script language="javascript" type="text/javascript" src="http://people.apache.org/~tomwhite/flot/jquery.js"></script> 
    <script language="javascript" type="text/javascript" src="http://people.apache.org/~tomwhite/flot/jquery.flot.js"></script> 
 </head> 
    <body> 
    <h1>%s Releases</h1> 
 
    <div id="placeholder" style="width:700px;height:%spx;"></div> 
 

<script id="source" language="javascript" type="text/javascript"> 
$(function () {

	var labels = new Object();
	
	function dt(date, version) {
		var timestamp = Date.parse(date);
		labels[timestamp] = version + " (" + date + ")";
		return timestamp
	}
	

    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
            border: '1px solid #fdd',
            padding: '2px',
            'background-color': '#fee',
            opacity: 0.80
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $("#placeholder").bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));
 
        if (true) {
            if (item) {
                if (previousPoint != item.datapoint) {
                    previousPoint = item.datapoint;
                    
                    $("#tooltip").remove();
                    var x = item.datapoint[0],
                        y = item.datapoint[1].toFixed(2);
                    
                    showTooltip(item.pageX, item.pageY, labels[x]);
                }
            }
            else {
                $("#tooltip").remove();
                previousPoint = null;            
            }
        }
    });
    
    $.plot($("#placeholder"), [ %s ], {
		xaxis: {
			mode: "time",
			max: (new Date()).getTime()
		},
		grid: { hoverable: true },
		points: { show: true },
		lines: { show: true }
	});
});
</script> 
 
 </body> 
</html>
""" % (project.title(), project.title(), len(minor_versions) * 30, ", ".join(z))