#!/bin/bash
user="root"
socket="/tmp/mysql_mha.sock"
cmd="mysql -u$user -S$socket -Dmonitor"
# 防止输出告警 mysql: [Warning] Using a password on the command line interface can be insecure
exists_increment=`MYSQL_PWD="mychebao" $cmd -e "select base from core_sqlrecord where date>date_format(DATE_ADD(now(),INTERVAL -30 minute),'%Y-%m-%d %H:%i:00');" |egrep -v base|wc -l`
if [ $exists_increment -ge 1 ];then 
db=$(MYSQL_PWD="mychebao" $cmd -e "select base from core_sqlrecord where date>=date_format(DATE_ADD(now(),INTERVAL -30 minute),'%Y-%m-%d %H:%i:00');" |egrep -v -w "base" |awk '{print $1}')
ddl=$(MYSQL_PWD="mychebao" $cmd -e '''select `sql` from core_sqlrecord where date>=date_format(DATE_ADD(now(),INTERVAL -30 minute),"%Y-%m-%d %H:%i:00");'''|egrep -v -w "sql"|egrep -i "alter|create|drop")

for ((i=1; i<=$exists_increment; i++))
do
newdb=$(MYSQL_PWD="mychebao" $cmd -e "select base from core_sqlrecord where date>=date_format(DATE_ADD(now(),INTERVAL -30 minute),'%Y-%m-%d %H:%i:00');"|egrep -v -w "base" |awk '{print $1}' | head -n"$i"|tail -1)
newddl=$(MYSQL_PWD="mychebao" $cmd -e '''select `sql` from core_sqlrecord where date>=date_format(DATE_ADD(now(), INTERVAL -30 minute),"%Y-%m-%d %H:%i:00");'''|egrep -v -w "sql" |egrep -i "alter|create|drop"| head -n"$i"| tail -1)
date=`date "+%Y-%m-%d %H:%M" ` 
if [ ! -d "/database/tmp/yearning/$newdb" ]; then  
    mkdir -p /database/tmp/yearning/$newdb  
fi  
echo "use $newdb;" >/database/tmp/yearning/${newdb}/${newdb}_$date.sql
echo "$newddl;" >>/database/tmp/yearning/${newdb}/${newdb}_$date.sql
done
fi
