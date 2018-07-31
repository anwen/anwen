数据库设计
========

保持简单
sudo service mongod start
sudo service mongod stop
mongod --auth -f /etc/mongod.conf --fork

--port 27017 --dbpath /data/db1
--dbpath=/var/lib/mongodb/
--smallfiles
--logpath=/data/db/log

db.enableFreeMonitoring()

sudo echo "never" >  /sys/kernel/mm/transparent_hugepage/defrag
[always] madvise never
