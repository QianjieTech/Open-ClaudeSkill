.PHONY: help install dev test clean build publish run example

help:
	@echo "Open-ClaudeSkill Makefile Commands:"
	@echo ""
	@echo "  make install    - Install the package"
	@echo "  make dev        - Install in development mode"
	@echo "  make test       - Run installation tests"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build distribution packages"
	@echo "  make publish    - Publish to PyPI (requires credentials)"
	@echo "  make run        - Run the MCP server"
	@echo "  make example    - Create example skills"
	@echo ""

install:
	pip install .

dev:
	pip install -e .
	@echo ""
	@echo "✅ Installed in development mode"
	@echo "Changes to source files will be reflected immediately"

test:
	python test_installation.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned build artifacts"

build: clean
	python -m build
	@echo "✅ Built distribution packages"

publish: build
	python -m twine upload dist/*
	@echo "✅ Published to PyPI"

run:
	python -m mcp_server_skill.server

example:
	mkdir -p .skill
	cp -r examples/calculator .skill/ 2>/dev/null || true
	cp -r examples/code-reviewer .skill/ 2>/dev/null || true
	@echo "✅ Created example skills in .skill/"
	@echo ""
	@echo "Available skills:"
	@ls -1 .skill/
