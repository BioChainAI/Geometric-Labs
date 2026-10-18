PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src$(if $(PYTHONPATH),:$(PYTHONPATH))

.PHONY: verify-all test-pillars vectors check-vectors bench clean
verify-all:
	$(PYTHON) verification/verify_geometric_labs_suite.py
	$(MAKE) test-pillars
	$(MAKE) check-vectors

test-pillars:
	$(PYTHON) -m unittest discover -s verification -p 'test_*.py' -v

vectors:
	$(PYTHON) spec_sync/generate_golden_vectors.py

check-vectors:
	$(PYTHON) spec_sync/generate_golden_vectors.py --check

bench:
	$(PYTHON) verification/verify_geometric_labs_suite.py

clean:
	find src verification spec_sync -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf build dist src/geometric_labs.egg-info
