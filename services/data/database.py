import sqlite3
from pathlib import Path


class Connection(sqlite3.Connection):
    def __exit__(self, *args):
        try:
            return super().__exit__(*args)
        finally:
            self.close()


def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path), timeout=10, factory=Connection)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("CREATE TABLE IF NOT EXISTS schema_versions(version INTEGER PRIMARY KEY)")
    applied = {row[0] for row in db.execute("SELECT version FROM schema_versions")}
    for migration in sorted((Path(__file__).resolve().parents[2] / "db/migrations").glob("[0-9]*.sql")):
        version = int(migration.name.split("_", 1)[0])
        if version not in applied:
            try:
                db.executescript("BEGIN IMMEDIATE;\n" + migration.read_text() +
                                 "\nINSERT OR IGNORE INTO schema_versions VALUES (%d);\nCOMMIT;" % version)
            except Exception:
                db.rollback()
                db.close()
                raise
    return db
