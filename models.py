import os, sys, json, shutil
from typing import List
from abc import ABC, abstractmethod
from firebase import *

class DIRef:
    def __init__(self, *subscripts: tuple[str]) -> None:
        self.subscripts = list(subscripts)
        
    def __str__(self) -> str:
        return "/".join(self.subscripts)

class DI:
    '''DatabaseInterface (DI) is a complex central interface managing all database operations.'''
    localFile = "database.json"
    syncStatus = False
    
    @staticmethod
    def setup():
        if not os.path.exists(os.path.join(os.getcwd(), DI.localFile)):
            with open(DI.localFile, "w") as f:
                json.dump({}, f)
        
        if FireRTDB.checkPermissions():
            try:
                if not FireConn.connected:
                    print("DI-FIRECONN: Firebase connection not established. Attempting to connect...")
                    response = FireConn.connect()
                    if response != True:
                        print("DI-FIRECONN: Failed to connect to Firebase. Aborting setup.")
                        return response
                    else:
                        print("DI-FIRECONN: Firebase connection established. Firebase RTDB is enabled.")
                else:
                    print("DI: Firebase RTDB is enabled.")
            except Exception as e:
                print("DI FIRECONN ERROR: " + str(e))
                return "Error"
            
        return True
    
    