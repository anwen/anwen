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

start:
	make test
	@echo "starting anwen"
	python3 hello.py


sync:
	scp -r devops aw:/var/www/anwen


test:
	@echo "starting test"
	python3 hello.py -t



backup:
	@echo "starting backup"
	fab backup

docs:
	python -m SimpleHTTPServer 8004



build:
	lessc -x --yui-compress static/less/main.less > static/css/main.css
	lessc -x --yui-compress static/less/ande.less > static/css/ande.css
	uglifyjs static/js/share.js -mc -o static/js/share.min.js



ci:
	@echo "starting commit"
	fab commit

deploy:
	@echo "starting deploy"
	fab deploy



ask:
	@echo "call ande"
	python ande/ask.py

add:
	@echo "starting add"
	git add .
