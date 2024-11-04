from models import *
DI.failoverStrategy = "efficient"
DI.setup()

data = {"name": "john", "last": "oliver"}
# DI.save(data, Ref("account"))
# DI.load(Ref("account"))

while True:
    try:
        exec(input("Code: "))
    except Exception as e:
        print(e)