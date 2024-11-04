import os, sys, json, shutil
from typing import List
from abc import ABC, abstractmethod
from firebase import *

class Ref:
    def __init__(self, *subscripts: tuple[str]) -> None:
        self.subscripts = list(subscripts)
        
    def __str__(self) -> str:
        return "/".join(self.subscripts)
    
class DIError:
    def __init__(self, message: str, supplementaryData: dict = None) -> None:
        self.message = message
        try:
            self.source = message[:message.index(":")]
        except:
            self.source = None
        self.supplementaryData = supplementaryData
        
    def __str__(self) -> str:
        return self.message

class DI:
    '''DatabaseInterface (DI) is a complex central interface managing all database operations.'''
    localFile = "database.json"
    failoverStrategy = "comprehensive" if not ('DI_FAILOVER_STRATEGY' in os.environ and os.environ.get('DI_FAILOVER_STRATEGY') == 'efficient') else 'efficient' # "comprehensive" or "efficient"
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
    
    @staticmethod
    def ensureLocalDBFile():
        if not os.path.isfile(os.path.join(os.getcwd(), DI.localFile)):
            with open(DI.localFile, "w") as f:
                json.dump({}, f)
        
        return
    
    @staticmethod
    def loadLocal(ref: Ref):
        DI.ensureLocalDBFile()
        
        data = None
        
        try:
            with open(DI.localFile, "r") as f:
                data = json.load(f)
        except Exception as e:
            print("DI LOADLOCAL ERROR: Failed to load JSON data from local file; error: {}".format(e))
            return DIError("DI LOADLOCAL ERROR: Failed to load data from local file.")
        
        try:
            for subscriptIndex in range(len(ref.subscripts)):
                data = copy.deepcopy(data[ref.subscripts[subscriptIndex]])
        except KeyError:
            return None
        except Exception as e:
            print("DI LOADLOCAL ERROR: Failed to retrieve target ref; error: {}".format(e))
            return DIError("DI LOADLOCAL ERROR: Failed to retrieve target ref.")
        
        return data

    @staticmethod
    def load(ref: Ref):
        # Check if Firebase is enabled
        if FireRTDB.checkPermissions():
            if not FireConn.connected:
                print("DI LOAD WARNING: FireRTDB is enabled but Firebase connection is not established; falling back to local...")
                return DI.loadLocal(ref)
        else:
            return DI.loadLocal(ref)
        
        ## Retrieve data from Firebase
        try:
            data = FireRTDB.getRef(str(ref))
            return data
        except Exception as e:
            DI.syncStatus = False
            print("DI LOAD WARNING: Failed to load from FireRTDB; error: '{}'. Falling back to local...".format(e))
            return DI.loadLocal(ref)