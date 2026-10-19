PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: help install test test-core demo
.DEFAULT_GOAL := help

help:
	@echo "make install    Créer .venv et installer les dépendances images"
	@echo "make test       Exécuter tous les tests (NumPy et OpenCV requis)"
	@echo "make test-core  Tester les TP sans dépendances externes"
	@echo "make demo       Générer les exemples dans outputs/"

install:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

test:
	$(PYTHON) -c "import numpy, cv2"
	$(PYTHON) -m unittest discover -s tests -v

test-core:
	$(PYTHON) -m unittest discover -s tests -p 'test_tp*.py' -v

demo:
	$(PYTHON) scripts/run_examples.py
