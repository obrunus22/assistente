from src.model.config import ConfigSchema
from src.model.users import UserSchema, PermissionSchema

def loadBoot():
    newName = None
    configs = ConfigSchema()
    users = UserSchema() # permissao esta dentro de users

    if not configs.list():
        newName = True
        cur = configs.con.cursor()
        cur.execute(f"INSERT INTO {configs.table}(ID, NAME) VALUES(1, 'Robô')")
        configs.con.commit()

    if not users.permission.list():
        cur = users.permission.con.cursor()
        cur.execute(f"INSERT INTO {users.permission.table}(NAME, NIVEL) VALUES('Responsável', 1)")
        cur.execute(f"INSERT INTO {users.permission.table}(NAME, NIVEL) VALUES('Amigo responsável', 2)")
        cur.execute(f"INSERT INTO {users.permission.table}(NAME, NIVEL) VALUES('Amigo', 3)")
        users.permission.con.commit()

    return [newName]