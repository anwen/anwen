mkdir data_backup/dbbackup_v3
mongodump -h 127.0.0.1 -d anwen -u aw -o data_backup/dbbackup_v3

cd data_backup
