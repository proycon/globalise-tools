.PHONY: setup frompagexml all
.DELETE_ON_ERROR:

#these can be injected/overriden via the environment:
PAGEXML_PATH = /home/proycon/exp/globalize-pagexml/

setup:
	@echo "Checking if common dependencies are available"
	command -V sed awk paste cat wc tee tr cut head tail python3
	@echo "Setting up Python virtual environment and installing globalise-tools"
	[ ! -e env ] && python3 -m venv env; source env/bin/activate; cd ../../; pip install .
	@echo "Activate the virtual environment with: source env/bin/activate , then run: make frompagexml PAGEXML_PATH=/path/to/globalise-pagexml && make all"

all: gm-aligned.store.stam.cbor

gm-aligned.store.stam.cbor:
	gt-align-rgp --verbose 2>&1 | tee gm-aligned.log

gm-aligned.tsv: gm-aligned.log
	grep "	" $< > $@

gm-aligned-lines.tsv: gm-aligned.store.stam.cbor
	gt-align-rgp-lines >$@ 

gm-nomatch.log: gm-nomatch.log
	grep "No match" $< > $@

frompagexml:
	#creates the lineinput_tsv files from pagexml, has to be invoked manually, ensure the gt-extract-lines.py script is linked and the virtualenv activated if needed
	gt-extract-lines -i $(PAGEXML_PATH) 
