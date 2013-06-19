安装说明
========


## Install

```bash
git clone https://github.com/anwen/anwen.git
cd anwen
sudo pip install -r conf/requirements.txt
sudo apt-get install mongodb  # other database will not be supported in a short time
```


## Start Anwen app

```bash
python hello.py -h  # you can find some help
python hello.py
```


## Testing

```bash
python tests.py
```

## Config

```bash
vi options/__init__.py
```

## set up a production enironment

supervisor and nginx config files are available in conf/
