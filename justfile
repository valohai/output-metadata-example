# Install project dependencies
dev:
    uv pip install -r requirements.txt

# Run an ad-hoc execution
adhoc:
    vh execution run --adhoc --title "dataset with random files" create-files

# Lint and type-check the project
lint:
    ruff format *.py
    mypy *.py
