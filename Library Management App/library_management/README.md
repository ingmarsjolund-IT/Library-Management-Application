
# Library Management (Tkinter + SQLite)

## Run
```bash
python -m library_management.interface.app
```

This will create `lbmms.db` in the package folder on first run.

## Project Layout
- `domain/` dataclasses for entities and view models
- `infrastructure/db/` SQLite database and repositories
- `application/` business logic + validation
- `interface/` Tkinter GUI

## Notes
- Member ID is optional on insert; leave blank to auto-generate.
- Error handling and validation show message boxes in the UI.
