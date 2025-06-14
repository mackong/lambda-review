.PHONY: layer
layer:
	@pip install -r requirements.txt -t python
	@zip -q -r layer.zip python/
	@rm -rf python
	@echo "layer.zip created, please upload to AWS as function layer."

.PHONY: code
code:
	@zip -q -r -j code.zip src/*
	@echo "code.zip created, please upload to AWS as function code."

