VENV_NAME=lebron-james
VENV_SHELL=$(VENV_NAME)/bin/activate

lebron:
	. $(VENV_SHELL) && python app.py

setup:
	make clean
	make pip-install
	make precommit

pip-install:
	rm -rf $(VENV_NAME)
	python3 -m venv $(VENV_NAME)
	. $(VENV_SHELL) && pip install pip-tools
	. $(VENV_SHELL) && pip install -r requirements.txt

precommit:
	. $(VENV_SHELL) && pre-commit install

clean:
	find . -name '__pycache__' -delete
	find . -name '*.pyc' -delete
