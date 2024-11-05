from models import *
DI.setup()
DI.save(None, Ref())

john = Identity('abc123', 'john', '123456', '2024-t2323r23r')
john.save()

while True:
    try:
        exec(input("Code: "))
    except Exception as e:
        print(e)