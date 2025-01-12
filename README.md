poetry init



How to run the local server
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```


If you have directly added dependency in pyproject.toml, you must run
```bash
poetry lock
```
before
```bash
poetry install
```
as this may retrun an error "pyproject.toml changed significantly since poetry.lock was last generated. Run `poetry lock [--no-update]` to fix the lock file."