from models import *
DI.setup()

john = Identity('abc123', 'john', '123456', '2024-t2323r23r')
# john.save()

while True:
    exec(input("Code: "))