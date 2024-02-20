import json
from src.model.users import UserSchema
import face_recognition as fr


class UserController(UserSchema):
    def __init__(self) -> None:
        super().__init__()
        self.loadList()

    def loadList(self) -> list:
        self.dataList = self.list()
        return self.dataList
        
    def get(self, user=None) -> None:
        data = self.list(user)

        if data:
            self.ID = data[0]["ID"]
            self.NAME = data[0]["NAME"]
            self.IDADE = data[0]["IDADE"]
            self.LANDMARKS = data[0]["LANDMARKS"]
            self.PERMISSION = data[0]["PERMISSION"]
            self.NIVEL = data[0]["NIVEL"]

    def setName(self, newName) -> str:
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.table} SET NAME = ? WHERE ID = ?", [newName, self.ID])
        self.con.commit()
        self.NAME = newName
        
        return self.NAME
    
    def getLandmarks(self, userId=None) -> list:
        users = self.list(userId)
        lendmarks = []
        
        if users:
            for user in users:
                lendmarks.append(json.loads(user["LANDMARKS"]))

        return lendmarks
    
    def findInFaces(self, faces:list) -> list:
        users = self.list(None, ["LANDMARKS"])

        for face in faces:
            for user in users:
                if fr.compare_faces([json.loads(user["LANDMARKS"])], face):
                    return user
                
        return []