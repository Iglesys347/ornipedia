# Ornipedia API

## Quick start

Install requirements

```bash
pip install -r requirements/requirements.txt
```

Start the API using uvicorn:

```bash
uvircorn src.main:app [--reload]
```

## Run tests

Install dev requirements

```bash
pip install -r requirements/dev-requirements.txt
```

Run the tests with `pytest`

```bash
pytest tests/
```

## Test coverage

Run tests with coverage

```bash
coverage run -m pytest tests/
```

Show coverage report

```bash
coverage report
```

Generate HTML coverage report (coverage report is generated in [htmlcov/index.html](htmlcov/index.html))

```bash
coverage html
```
