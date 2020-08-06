class Calc():

    def __init__(self, one, two):
        self.one = int(one)
        self.two = int(two)

    def sloz(self):
        print(self.one + self.two)


my_c = Calc(1, 6)
my_c.sloz()
