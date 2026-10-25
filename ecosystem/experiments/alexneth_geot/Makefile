PYTHON ?= python3
.PHONY: test research-tests interop verify
# Invoke with PYTHON=/workspace/.venvs/alexneth-geot/bin/python in this instance.
test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v
research-tests:
	$(PYTHON) -m unittest discover -s research/tests -p 'test_*.py' -v
interop:
	$(PYTHON) tools/interop.py
verify:
	$(PYTHON) tools/verify.py
