class Person:
    def __init__(self, name, height):
        self.name = name
        self.height = height
        if self.height > 2.0:
            print("вы гигант")

# Примеры:
p1 = Person("Семён", 1.75)
p2 = Person("Максим", 2.1)