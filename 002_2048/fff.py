
from random import randint

class T:
    ax = 3
    def __init__(self):
        self.fa = 3

    def get(self):
        return randint(1,5)


    def ppp(self):
        print(self.get(), self.get())




t = T()
t.ppp()