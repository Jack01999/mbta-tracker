develop:
	python3 -m venv venv
	. venv/bin/activate; pip3 install -r requirements.txt

format:
	. venv/bin/activate; isort controller
	. venv/bin/activate; black controller

run:
	. venv/bin/activate; python3 -m controller

sim:
	. venv/bin/activate; python3 -m controller simulate

