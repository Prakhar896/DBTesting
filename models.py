import os, json
from typing import List, Dict, Any
from database import *

class Identity(DIRepresentable):
    def __init__(self, id, username, password, created) -> None:
        self.originRef = Identity.generateRef(id)
        self.id = id
        self.username = username
        self.password = password
        self.created = created
    
    @staticmethod
    def load(id=None, username=None) -> 'Identity | list[Identity] | None':
        data = DI.load(Identity.generateRef(id))
        if isinstance(data, DIError):
            return data

        return Identity(
            id=data['id'],
            username=data['username'],
            password=data['password'],
            created=data['created']
        )
    
    def represent(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'created': self.created
        }
    
    def save(self) -> bool:
        convertedData = self.represent()
        
        return DI.save(convertedData, self.originRef)
    
    @staticmethod
    def generateRef(id) -> Ref:
        return Ref("accounts", id)