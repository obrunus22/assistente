from src.database import Database

_table = "CONFIG"
_columns = {
    "ID":"INTEGER PRIMARY KEY AUTOINCREMENT",
    "NAME":"VARCHAR(30)",
    "LANGUAGE":"VARCHAR(20)",
    "VOICEHUMAN":"VARCHAR(30)",
    "DEVICEINDEX":"INTEGER",
}

class ConfigSchema(Database):
    def __init__(self) -> None:
        super().__init__(_table, _columns)

        cur = self.con.cursor()
        resp = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [_table])

        if not resp.fetchone():
            self.createTables()
