class Animal:
	name: str
	
	def __init__(self, name: str):
		self.name = name
	
	def speak(self) -> str:
		raise NotImplementedError
	
	def reply(self) -> str:
		return self.speak()

class Mammal(Animal):
	def __init__(self, name: str):
		super().__init__(name)
	
	def speak(self) -> str:
		raise NotImplementedError

class Dog(Mammal):
	def __init__(self, name: str):
		super().__init__(name)
	
	def speak(self) -> str:
		return f"{self.name} says Woof!"

class Cat(Mammal):
	def __init__(self, name: str):
		super().__init__(name)
	
	def speak(self) -> str:
		return f"{self.name} says Meow!"

class Primate(Mammal):
	def __init__(self, name: str):
		super().__init__(name)
	
	def speak(self) -> str:
		return f"{self.name} says Ooh ooh ah ah!"

class ComputerScientist(Primate):
	def __init__(self, name: str):
		super().__init__(name)

