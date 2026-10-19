PYTHON ?= python3
ROOT := $(abspath ..)
export PYTHONDONTWRITEBYTECODE := 1
.PHONY: help list doctor sync geometry test integration protocol-compatibility demo lock check-lock acceptance
help:
	@echo 'Additive ecosystem: list doctor sync test integration protocol-compatibility demo geometry lock check-lock acceptance'
list:
	$(PYTHON) tools/glab.py list
doctor:
	$(PYTHON) tools/glab.py doctor
sync:
	$(PYTHON) tools/glab.py sync
geometry:
	$(MAKE) -C $(ROOT) verify-all
test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v
integration:
	$(PYTHON) -m unittest discover -s integration_tests -p 'test_*.py' -v
protocol-compatibility:
	$(PYTHON) tools/protocol_compatibility.py
demo:
	$(PYTHON) simulator/reference_mesh.py
lock:
	$(PYTHON) tools/glab.py lock
check-lock:
	$(PYTHON) tools/glab.py check-lock
acceptance:
	$(PYTHON) tools/run_acceptance.py
