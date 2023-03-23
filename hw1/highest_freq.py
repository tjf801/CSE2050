from __future__ import annotations

from letters import letter_count, letter_frequency


def highest_freq(file_path: str) -> tuple[str, float]:
	"""returns the highest frequency letter appearing in a given file, along with its frequency."""
	return max( # return the maximum...
		letter_frequency(letter_count(file_path)).items(), # using the letter frequency dict...
		key=lambda x: x[1] # sorted by the frequency
	)


def __run_tests():
	assert highest_freq('./hw1/frost.txt') == ('e', 0.10952380952380952)

if __name__=="__main__": __run_tests()