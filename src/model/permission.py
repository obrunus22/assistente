from src.database import Database

_table = "PERMISSION"
_columns = {
    "ID":"INTEGER PRIMARY KEY AUTOINCREMENT",
    "NAME":"VARCHAR(30)",
    "NIVEL":"INTEGER NOT NULL DEFAULT 0",
}

class PermissionSchema(Database):
    def __init__(self) -> None:
        super().__init__(_table, _columns)

        cur = self.con.cursor()
        resp = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [_table])

        if not resp.fetchone():
            self.createTables()