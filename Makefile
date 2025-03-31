.PHONY: install
install:
	uv build

.PHONY: format
format:
	find src -name "*.py" | xargs black
