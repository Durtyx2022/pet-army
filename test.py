class Pet:
    def __init__(self, name, age, category, hunger_bar):
        self.name = name
        self.age = age
        self.category = category
        self.hunger_bar = hunger_bar

    def feed(self, food):
        if food == "fruit":
            self.hunger_bar = self.hunger_bar + 1
        elif food == "meat":
            self.hunger_bar = self.hunger_bar + 2
        elif food == "boar_meat":
            self.hunger_bar = self.hunger_bar - 1
        elif food == "lasania":
            if self.name == "garfield":
                self.hunger_bar = self.hunger_bar + 5
            else:
                self.hunger_bar = self.hunger_bar - 2


garfield = Pet(name="garfield", age=2, category="cat", hunger_bar=0)
penny = Pet(name="penny", age=8, category="cat", hunger_bar=7)
snow = Pet(name="snow", age=6, category="dog", hunger_bar=2)

pets = [garfield, penny, snow]


def feed_hunger_pets(pets, critical_hunger_level, food):
    for pet in pets:
        if pet.hunger_bar < critical_hunger_level:
            print(f"{pet.name} is hungry! its hunger bar is: {pet.hunger_bar}")
            pet.feed(food=food)
            print(f"I feed {pet.name}. now its hunger bar is: {pet.hunger_bar}")


feed_hunger_pets(pets=pets, critical_hunger_level=5, food="fruit")