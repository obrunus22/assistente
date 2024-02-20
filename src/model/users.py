from src.model.permission import PermissionSchema
from src.database import Database

_table = "USERS"
_columns = {
    "ID":"INTEGER PRIMARY KEY AUTOINCREMENT",
    "NAME":"VARCHAR(30)",
    "IDADE":"INTEGER",
    "LANDMARKS":"TEXT",
    "PERMISSION":"INTEGER REFERENCES=PERMISSION",
}

class UserSchema(Database):
    def __init__(self) -> None:
        super().__init__(_table, _columns)
        self.permission = PermissionSchema()

        cur = self.con.cursor()
        resp = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [_table])

        if not resp.fetchone():
            self.createTables()

    def list(self, id=None, columns:list=[]) -> list:
        try:
            cur = self.con.cursor()

            sql = """
                SELECT U.ID, U.NAME, U.IDADE, U.LANDMARKS, P.NAME AS PERMISSAO, P.NIVEL FROM USERS AS U
                JOIN PERMISSION AS P ON(P.ID = U.PERMISSION)
            """

            if id is not None:
                sql = sql + f" WHERE U.ID = {id}"

            resp = cur.execute(sql)
            data = resp.fetchall()

            if data:
                dataObj = []

                for el in data:
                    dataObj.append({
                        "ID":el[0],
                        "NAME":el[1],
                        "IDADE":el[2],
                        "LANDMARKS":el[3],
                        "PERMISSAO":el[4],
                        "NIVEL":el[5],
                    })

                if len(columns) > 0:
                    for newData in dataObj:
                        obj = {}
                        for column in columns:
                            obj[column] = newData[column]
                    
                    return obj
                
                return dataObj
            return []
        except Exception as e:
            print(e)