运行
========

## Install
- please use python3

```bash
# sys 2.3G
apt autoremove
apt-get update
apt-get upgrade
# apt-get install build-essential
# apt-get install python3
apt-get install python3-dev
apt-get install python-imaging
apt-get install python3-pil
# apt-get install mongodb
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org


git clone https://github.com/anwen/anwen.git
cd anwen
sudo pip3 install -r conf/requirements.txt
sudo pip install -r conf/requirements.txt


python tests.py # Testing
python hello.py -h  # you can find some help
python hello.py # Start Anwen app



vi options/__init__.py  ## Config
## set up a production enironment
supervisor and nginx config files are available in conf/



```
