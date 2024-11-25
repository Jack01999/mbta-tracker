develop:
	python3 -m venv venv --system-site-packages
	. venv/bin/activate; pip3 install -r requirements.txt

format:
	. venv/bin/activate; isort .
	. venv/bin/activate; black .

run:
	. venv/bin/activate; python3 -m controller

sim:
	. venv/bin/activate; python3 -m controller simulate

