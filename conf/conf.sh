# config
sudo npm install -g less
sudo npm install -g uglify-js

# 由于使用了webservice，nginx需要重新编译新的模块才能支持，使用了haproxy。
# haproxy来监听80端口，将http请求转发至82端口并由nginx来监听。

# for centos-vps:
rpm -ivh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm

yum -y install haproxy
scp ~/develop/anwen/conf/haproxy.cfg aw:/etc/haproxy/haproxy.cfg
/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg

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
db.addUser('sa','key')   
use anwen
db.auth("aw", "key")
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

# deploy at server:
mkdir /var/www/anwen
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
git remote rm pro
git remote add pro aaw:/var/www/anwen/
git push pro

scp options/server_setting.py aaw:/var/www/anwen/options
scp -r static/upload/img aaw:/var/www/anwen/static/upload/
scp db/data/User.yaml aaw:/var/www/anwen/db/data/
scp db/data/Admin.yaml aaw:/var/www/anwen/db/data/

# scp conf/nginx.conf aw:/usr/local/nginx/conf/nginx.conf
scp conf/nginx.conf aaw:/etc/nginx
/etc/init.d/nginx reload

mkdir /home/anwen

scp conf/supervisord.conf aaw:/etc/supervisord.conf
for i in {1..2}
    do supervisorctl -c supervisord.conf restart anwen:anwen$i
done
supervisorctl restart all