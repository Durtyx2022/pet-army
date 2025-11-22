class Pet:
    def __init__(self, name, age, category, hunger_bar,favorite_food):
        self.name = name
        self.age = age
        self.category = category
        self.hunger_bar = hunger_bar
        self.favorite_food = favorite_food

    def feed(self, food,favorite_food):
        if food == "fruit":
            self.hunger_bar = self.hunger_bar + 1
        elif food == "meat":
            self.hunger_bar = self.hunger_bar + 3
        elif food == "boar_meat":
            self.hunger_bar = self.hunger_bar - 1
        elif food == "lasania":
            if self.name == "garfield":
                self.hunger_bar = self.hunger_bar + 5
            else:
                self.hunger_bar = self.hunger_bar - 2
        if food == favorite_food:
            self.hunger_bar = self.hunger_bar + 4

garfield = Pet(name="garfield", age=2, category="cat", hunger_bar=0, favorite_food="lasania")
penny = Pet(name="penny", age=8, category="cat", hunger_bar=7, favorite_food="meat")
snow = Pet(name="snow", age=6, category="dog", hunger_bar=2,favorite_food="fruit")

pets = [garfield, penny, snow]
pets_favorite_food = ["lasania", "meat", "fruit"]

def feed_hunger_pets(pets, critical_hunger_level, food):
    for pet in pets:
        if pet.hunger_bar < critical_hunger_level:
            print(f"{pet.name} is hungry! its hunger bar is: {pet.hunger_bar}")
            pet.feed(food=food,favorite_food=pet.favorite_food)
            print(f"I feed {pet.name}. now its hunger bar is: {pet.hunger_bar}")


feed_hunger_pets(pets=pets, critical_hunger_level=5, food="lasania")