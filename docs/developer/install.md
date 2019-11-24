安装 install
========


## Install
- we suggest use python3

```bash
apt autoremove
apt-get update
apt-get upgrade
# apt-get install build-essential python3
# apt-get remove python-pip
# apt-get remove python3-pip -y
apt-get install python3-pip
apt-get install python3-dev
# apt-get build-dep python-lxml
# apt-get install python-imaging
apt-get install python3-pil
apt install git
apt install nginx
apt install supervisor
apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
apt install tmux
apt install unzip


# bad
# pip3 install --upgrade pip
# curl https://bootstrap.pypa.io/get-pip.py | python3

# sudo dpkg-reconfigure locales
# export LC_ALL="en_US.UTF-8"
# export LC_CTYPE="en_US.UTF-8" # zh_CN.UTF-8
# export LC_ALL=C
# export LANGUAGE="en_US.UTF-8"


# install mongodb
# sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

sudo apt-get update
sudo apt-get install -y mongodb-org

cd /var/www
git clone https://github.com/anwen/anwen.git
cd anwen
sudo pip3 install -r conf/requirements.txt

python3 tests.py # Testing
python3 hello.py -h  # you can find some help
python3 hello.py # Start Anwen app


## set up a production enironment
supervisor and nginx config files are available in conf/

```
