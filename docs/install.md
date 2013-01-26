安装说明
========


## Install

```bash
git clone https://github.com/anwen/anwen.git
cd anwen
sudo pip install -r conf/requirements.txt
sudo apt-get install mongodb  # We turn to mongodb form sql, we may use sqlite again
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

## set up a production enironment

supervisor and nginx config files are available in conf/
