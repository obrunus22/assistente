from src.model.config import ConfigSchema

class ConfigController(ConfigSchema):
    def __init__(self) -> None:
        super().__init__()
        self.get(1)

    def get(self, id:int):
        data = self.list(id)

        if data:
            self.ID = data["ID"]
            self.NAME = data["NAME"]
            self.LANGUAGE = data["LANGUAGE"]
            self.VOICEHUMAN = data["VOICEHUMAN"]
            self.DEVICEINDEX = data["DEVICEINDEX"]
        
    def loadValues(self):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.table}(NAME) VALUES('Robô')")
        self.con.commit()

    def setName(self, newName):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.table} SET NAME = ? WHERE ID = ?", [newName, self.ID])
        self.con.commit()
        self.NAME = newName

    def setDeviceIndex(self, index:int) -> None:
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.table} SET DEVICEINDEX = ? WHERE ID = ?", [index, self.ID])
        self.con.commit()
        self.DEVICEINDEX = index
    