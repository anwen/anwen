安装说明 install
========


## Install

```bash
git clone https://github.com/askender/anwen.in.git
cd anwen.in
sudo pip install -r conf/requirements.txt
```

## Start Anwen service
### edit db/db_config.py to choose database type

* if you choose mysql, you should install mysql, open mysql service and create a database which name in db_config.
* python hello.py -h  # you can find some help

```bash
python hello.py -c
python hello.py
```

## Testing

```bash
python tests.py
```