help:
	@echo Usage: make [\TARGET\]
	@echo
	@echo TARGET:
	@echo "    clean    清理临时文件"
	@echo "    test     anwen test"
	@echo "    docs     anwen docs"
	@echo "    start    start anwen"
	@echo "    deploy   deploy anwen"
	@echo


.PHONY: clean docs test start deploy

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

docs:
	python -m SimpleHTTPServer 8004

test:
	@echo "starting test"
	python hello.py -t

start:
	make test
	@echo "starting anwen"
	python hello.py

deploy:
	@echo "starting deploy"
	fab deploy

backup:
	@echo "starting backup"
	fab back_data