import sqlite3

class Database:
    def __init__(self, table, columns) -> None:
        self.con = sqlite3.connect("src/db/mind.db", check_same_thread=False)
        self.table = table
        self.columns = columns

    def list(self, id=None, columns:list=[]) -> list:
        try:
            columns = ', '.join(str(key) for key in self.columns)
            cur = self.con.cursor()
            sql = f"SELECT {columns} FROM {self.table}"

            if id:
                sql = sql + f" WHERE ID = {id}"

            resp = cur.execute(sql)
            data = resp.fetchall()

            if data:
                dataObj = []

                for el in data:
                    obj = {}

                    i=0
                    for key in self.columns:
                        obj[key] = el[i]
                        i = i+1

                    dataObj.append(obj)

                if len(self.columns) > 0:
                    for newData in dataObj:
                        obj = {}
                        for column in self.columns:
                            obj[column] = newData[column]
                    
                    return obj
                
                return dataObj

            return []
        except Exception as e:
            print("Algo deu errado list(): {}".format(e))

    def createTables(self) -> None:
        try:
            columns = []
            for key in self.columns:
                if "REFERENCES=" in self.columns[key]:
                    type, ref = self.columns[key].split("REFERENCES=")
                    columns.append(f"{key} {type}")
                    columns.append(f"FOREIGN KEY({key}) REFERENCES {ref}(ID)")
                    continue

                columns.append(f"{key} {self.columns[key]}")

            columns = ', '.join(str(key) for key in columns)
            cur = self.con.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table}({columns});")

            self.con.commit()
        except Exception as e:
            print("Algo deu errado createTables(): {}".format(e))

    def add(self, column, value):
        try:
            cur = self.con.cursor()
            if type(column) == list:
                columns = ', '.join(str(key).upper() for key in column)
                values = ', '.join('?' for key in value)
                sql = f"INSERT INTO {self.table}({columns}) VALUES({values});"
                insert = cur.execute(sql, value)
            else:
                sql = f"INSERT INTO {self.table}({column}) VALUES(?);"
                insert = cur.execute(sql, [value])

            self.con.commit()
        except Exception as e:
            print(e)


    # def getColumn(self) -> list:
    #     try:
    #         cur = self.con.cursor()
    #         resp = cur.execute("PRAGMA table_info(CONFIG);")
    #         data = resp.fetchall()

    #         if data:
    #             columns = []
    #             for column in data:
    #                 columns.append({"name":column[1], "type":column[2]})

    #             self.columns = columns

    #         return self.columns
    #     except Exception as e:
    #         print("Algo deu errado no getColumn(): {}".format(e))
        

    def get():
        pass
