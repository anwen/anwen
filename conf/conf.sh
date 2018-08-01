# config
scp options/server_setting.py aw:/var/www/anwen/options
# sync data
scp -r static/upload/img aw:/var/www/anwen/static/upload/
scp db/data/User.yaml aw:/var/www/anwen/db/data/
scp db/data/Admin.yaml aw:/var/www/anwen/db/data/
# import data
cd /var/www/anwen
cd db
python3 db_in_out.py -o
python3 db_in_out.py -i -n all
python3 db_in_out.py -i

# deploy at server:
mkdir /var/www/anwen
cd /var/www/anwen
git init .
git config receive.denyCurrentBranch ignore
git config --bool receive.denyNonFastForwards false
cd .git/hooks
# wget http://utsl.gen.nz/git/post-update
scp conf/post-update aw:/var/www/anwen/.git/hooks
chmod +x post-update
# after push
cd ../..
git checkout master

at local:
git remote rm ol
git remote add ol aw:/var/www/anwen/
git push ol

# scp conf/nginx.conf aw:/usr/local/nginx/conf/nginx.conf
scp conf/nginx.conf aw:/etc/nginx
/etc/init.d/nginx reload

mkdir /home/anwen
service supervisord start
service supervisor  start
service supervisor restart

sudo killall supervisord
scp conf/supervisord.conf aw:/etc/supervisord.conf
for i in {1..2}
    do supervisorctl -c supervisord.conf restart anwen:anwen$i
done
supervisorctl restart all









# config front
sudo npm install -g less
sudo npm install -g uglify-js
# 由于使用了webservice，nginx需要重新编译新的模块才能支持，使用了haproxy。
# haproxy来监听80端口，将http请求转发至82端口并由nginx来监听。

# check disk
df -lh
ls -sSh
du -s ./*|sort -rn
