PYTHON ?= python3
PORT ?= 8080
LIB := $(PYTHON) tools/library.py

.PHONY: serve check test index list new ingest track lock-ide archive-index archive-list

# Serve the IDE at http://localhost:$(PORT)/ (localhost only).
serve:
	$(PYTHON) -m http.server $(PORT) --bind 127.0.0.1

check:
	$(LIB) check
	$(PYTHON) tools/archive.py check
	$(PYTHON) tools/releases.py check
	$(MAKE) test

test:
	$(PYTHON) -m unittest discover -s tests -v

index:
	$(LIB) index
	$(PYTHON) tools/archive.py index
	$(PYTHON) tools/releases.py index

archive-index:
	$(LIB) index
	$(PYTHON) tools/archive.py index

archive-list:
	$(PYTHON) tools/archive.py list

list:
	$(LIB) list

# Usage: make new SLUG=fifteen-lemmas TITLE="The Fifteen Lemmas" [TIER=core]
new:
	@test -n "$(SLUG)" -a -n "$(TITLE)" || { echo 'usage: make new SLUG=<kebab-case> TITLE="<title>" [TIER=core|series|external]'; exit 2; }
	$(LIB) new --slug "$(SLUG)" --title "$(TITLE)" --tier "$(or $(TIER),external)"

# Usage: make ingest PAPER=RP-0001   (sorts every file in inbox/)
ingest:
	@test -n "$(PAPER)" || { echo 'usage: make ingest PAPER=RP-0001'; exit 2; }
	$(LIB) ingest "$(PAPER)"

# Usage: make track PAPER=RP-0001   (records files you placed in the paper by hand)
track:
	@test -n "$(PAPER)" || { echo 'usage: make track PAPER=RP-0001'; exit 2; }
	$(LIB) track "$(PAPER)"

lock-ide:
	$(LIB) lock-ide
