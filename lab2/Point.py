from __future__ import annotations

class Point:
	def __init__(self, x: int | float, y: int | float):
		self.x = x
		self.y = y
	
	def __str__(self) -> str:
		return f"Point({self.x}, {self.y})"
	
	def dist_from_origin(self) -> float:
		return (self.x * self.x + self.y * self.y) ** 0.5
	
	def __eq__(self, other: Point) -> bool:
		return self.dist_from_origin() == other.dist_from_origin()
	def __lt__(self, other: Point) -> bool:
		return self.dist_from_origin() < other.dist_from_origin()
	def __gt__(self, other: Point) -> bool:
		return self.dist_from_origin() > other.dist_from_origin()


def __run_tests():
	# test __str__
	assert str(Point(1, 2)) == "Point(1, 2)"
	
	# test __eq__
	assert Point(1, 2) == Point(1, 2)
	assert Point(1, 2) != Point(2, 1)
	
	# test __lt__
	assert Point(1, 2) < Point(10, 20)
	assert not Point(10, 20) < Point(1, 2)
	
	# test __gt__
	assert Point(10, 20) > Point(1, 2)
	assert not Point(1, 2) > Point(10, 20)
	
	# test dist_from_origin
	assert Point(3, 4).dist_from_origin() == 5.0
	assert Point(0, 0).dist_from_origin() == 0.0

if __name__ == "__main__": __run_tests()