from models import *
DI.setup()
import time
time.sleep(10)
a = DI.load(Ref("c"))
print(a)

while True:
    exec(input("Enter code: "))