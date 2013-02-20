help:
	@echo Usage: make [\TARGET\]
	@echo
	@echo TARGET:
	@echo "    clean    清理临时文件"
	@echo "    test     a test"
	@echo "    start    start anwen"
	@echo "    deploy   deploy anwen"
	@echo


.PHONY: clean-pyc clean-build docs

clean: clean-build clean-pyc


clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


test:
	@echo "starting test"
	python hello.py -t

start:
	@echo "starting anwen"
	python hello.py

deploy:
	@echo "starting deploy"
	fab prepare_deploy

docs:
	$(MAKE) -C docs html

install:
	python setup.py install
