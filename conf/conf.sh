# config
sudo npm install -g less
sudo npm install -g uglify-js


scp conf/nginx.conf aw:/usr/local/nginx/conf/nginx.conf
/etc/init.d/nginx reload
scp aw:/var/www/anwen/options/server_setting.py ~/
scp ~/develop/anwen_begin/options/server_setting.py aw:/var/www/anwen/options/server_setting.py 



# 由于使用了webservice，nginx需要重新编译新的模块才能支持，使用了haproxy。
# haproxy来监听80端口，将http请求转发至82端口并由nginx来监听。

# for centos-vps:
rpm -ivh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm

yum -y install haproxy
scp ~/develop/anwen/conf/haproxy.cfg aw:/etc/haproxy/haproxy.cfg
/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg

scp ~/develop/anwen/conf/supervisord.conf aw:/etc/supervisord.conf
for i in {6..9}
    do supervisorctl -c supervisord.conf restart anwen:myapp$i
done

# For 64-bit yum源配置：
vi /etc/yum.repos.d/10gen.repo
	[10gen]
	name=10gen Repository
	baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
	gpgcheck=0
	enabled=1

yum info mongo-10gen-server
yum install mongo-10gen-server

# windows：
# I:\tools\mongo\mongod.exe --logpath I:\tools\mongo\logs\mongodb.log --logappend --dbpath I:\tools\mongo\data --directoryperdb --serviceName MongoDB --install
# net start MongoDB
# linux:
mongod --dbpath=/var/lib/mongodb/ --smallfiles --fork --logpath=/data/db/log --auth
mongoexport



# db update
cd /var/www/anwen
./db_in_out -o
mongo
use admin
db.system.users.find()
db.addUser('sa','sa')   
use anwen
db.auth("aw", "")
db.getCollectionNames()
db.Admin_Col.drop()
db.Comment_Col.drop()
db.Feedback_Col.drop()
db.Hit_Col.drop()
db.Share_Col.drop()
db.Tag_Col.drop()
db.User_Col.drop()
./db_in_out -i

# check disk
df -lh
ls -sSh
du -s ./*|sort -rn


# LNMP状态管理： /root/lnmp {start|stop|reload|restart|kill|status}
# Nginx状态管理：/etc/init.d/nginx {start|stop|reload|restart}
# PHP-FPM状态管理：/etc/init.d/php-fpm {start|stop|quit|restart|reload|logrotate}
# PureFTPd状态管理： /etc/init.d/pureftpd {start|stop|restart|kill|status}
# MySQL状态管理：/etc/init.d/mysql {start|stop|restart|reload|force-reload|status}
# Memcached状态管理：/etc/init.d/memcached {start|stop|restart}

deploy at server:
cd /var/www/anwen
git init .
git config receive.denyCurrentBranch ignore
git config --bool receive.denyNonFastForwards false
cd .git/hooks
wget http://utsl.gen.nz/git/post-update
chmod +x post-update
# after push
cd ../..
git checkout master

at local:
git remote rm prod
git remote add prod root@113.11.199.77:/var/www/anwen/
git push prod

