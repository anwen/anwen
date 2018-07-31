数据库设计
========

保持简单
sudo service mongod start
db.enableFreeMonitoring()

sudo echo "never" >  /sys/kernel/mm/transparent_hugepage/defrag
[always] madvise never
