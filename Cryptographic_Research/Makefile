PYTHON ?= python3
ITEMS := $(sort $(wildcard experimental/CR-*/ published/CR-*/))

.PHONY: check registry test test-tools test-items check-vectors list new demo-cr0001

check: registry test check-vectors

registry:
	$(PYTHON) tools/registry.py check

list:
	$(PYTHON) tools/registry.py list

test: test-tools test-items

test-tools:
	$(PYTHON) -m unittest discover -s tests -v

test-items:
	@set -e; for item in $(ITEMS); do \
		echo "== $$item"; \
		(cd $$item && $(PYTHON) -m unittest discover -s tests -v); \
	done

check-vectors:
	@set -e; for item in $(ITEMS); do \
		if [ -f $$item/vectors/generate_vectors.py ]; then \
			$(PYTHON) $$item/vectors/generate_vectors.py --check; \
		fi; \
	done

# Usage: make new SLUG=merkle-signature TITLE="Merkle signatures"
new:
	@test -n "$(SLUG)" -a -n "$(TITLE)" || { echo 'usage: make new SLUG=<kebab-case> TITLE="<title>"'; exit 2; }
	$(PYTHON) tools/registry.py new --slug "$(SLUG)" --title "$(TITLE)"

demo-cr0001:
	$(PYTHON) experimental/CR-0001_lamport-otp/demo.py --length 5 --seed demo
