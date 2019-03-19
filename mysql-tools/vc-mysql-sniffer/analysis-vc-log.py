#!/usr/bin/python
#coding:utf8
# python analysis-vc-log.py 3306 60 | sort | uniq -c | sort -nr |head -n 10
import re
import sys
import os
import commands
#vc_sniffer_time=60
port=sys.argv[1]
vc_sniffer_time=sys.argv[2]
vc_cmd=""" /usr/bin/timeout %s  /usr/local/vc-mysql-sniffer/vc-mysql-sniffer -binding="[::]:%s"  > /tmp/tmp_vc_mysql_%s.txt """ % (vc_sniffer_time,port,port)
outtext = commands.getoutput(vc_cmd)
cmd=""" grep -Ev '# Time:|# User@Host' /tmp/tmp_vc_mysql_%s.txt |sed 's/# Query_time.*/myxxxxx/g' |awk BEGIN{RS=EOF}'{gsub(/\\n/," ");print}'|awk BEGIN{RS=EOF}'{gsub(/myxxxxx/,"\\n");print}' >/tmp/vc_mysql_%s.txt""" % (port,port)
outtext = commands.getoutput(cmd)
file="/tmp/vc_mysql_%s.txt" % (port)
logFo = open(file)
for line in logFo:
    line = re.sub(r"\n","",line)
    lineMatch = re.match(r".*",line)
    if lineMatch:
        lineTmp = lineMatch.group(0)
        lineTmp = lineTmp.lower()
        # remove extra space
        lineTmp = re.sub(r"\s+", " ",lineTmp)
        # replace values (value) to values (x)
        lineTmp = re.sub(r"values\s*\(.*?\)", "values (x)",lineTmp)
        # replace filed = 'value' to filed = 'x'
        lineTmp = re.sub(r"(=|>|<|>=|<=)\s*('|\").*?\2","\\1 'x'",lineTmp)
        # replace filed = value to filed = x
        lineTmp = re.sub(r"(=|>|<|>=|<=)\s*[0-9]+","\\1 x",lineTmp)
        # replace like 'value' to like 'x'
        lineTmp = re.sub(r"like\s+('|\").*?\1","like 'x'",lineTmp)
        # replace in (value) to in (x)
        lineTmp = re.sub(r"in\s+\(.*?\)","in (x)",lineTmp)
        # replace between '...' and '...' to between 'x' and 'x'
        lineTmp = re.sub(r"between\s+('|\").*?\1\s+and\s+\1.*?\1","between 'x' and 'x' ",lineTmp)
        # replace between ... and ... to between x and x
        lineTmp = re.sub(r"between\s+[0-9]+\s+and\s+[0-9]+","between x and x ",lineTmp)
        # replace limit x,y to limit
        lineTmp = re.sub(r"limit.*","limit",lineTmp)
        print lineTmp
logFo.close()
