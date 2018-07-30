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

build:
	lessc -x --yui-compress static/less/main.less > static/css/main.css
	lessc -x --yui-compress static/less/ande.less > static/css/ande.css
	uglifyjs static/js/share.js -mc -o static/js/share.min.js

start:
	make test
	@echo "starting anwen"
	python hello.py

ci:
	@echo "starting commit"
	fab commit

deploy:
	@echo "starting deploy"
	fab deploy

backup:
	@echo "starting backup"
	fab back_data

ask:
	@echo "call ande"
	python ande/ask.py

add:
	@echo "starting add"
	git add .
