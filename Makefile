:PHONY setup
setup:
	mkdir -p sql-copilot/backend/ai
	cd sql-copilot/backend
	python3 -m venv venv
	source venv/bin/activate

