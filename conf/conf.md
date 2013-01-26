配置
========

由于使用了webservice，nginx需要重新编译新的模块才能支持，使用了haproxy。
haproxy来监听80端口，将http请求转发至82端口并由nginx来监听。

以下为一些记录：
目前所用的centos-vps需要：
rpm -ivh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
yum -y install haproxy
scp ~/anwen/conf/haproxy.cfg aw:/etc/haproxy/haproxy.cfg
scp ~/anwen/conf/supervisord.conf aw:/etc/supervisord.conf

