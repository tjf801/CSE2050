from __future__ import annotations

import string


def letter_count(file_path: str) -> dict[str, int]:
	"""Return a dictionary of letter counts from a file."""
	with open(file_path) as file:
		file_text: str = file.read().lower() # only read the file once for performance purposes
		return {letter: file_text.count(letter) for letter in 'abcdefghijklmnopqrstuvwxyz'}

def letter_frequency(frequency_dict: dict[str, int]) -> dict[str, float]:
	"""Returns a dictionary of letter frequencies from a dictionary of letter counts."""
	total_letters: int = sum(frequency_dict.values())
	return {letter: count/total_letters for letter, count in frequency_dict.items()}


def __run_tests():
	assert letter_count('./hw1/frost.txt') == {
		'a': 13,
		'b': 2,
		'c': 6,
		'd': 10,
		'e': 23,
		'f': 12,
		'g': 2,
		'h': 12,
		'i': 23,
		'j': 0,
		'k': 2,
		'l': 6,
		'm': 3,
		'n': 9,
		'o': 20,
		'p': 1,
		'q': 0,
		'r': 14,
		's': 14,
		't': 20,
		'u': 5,
		'v': 2,
		'w': 8,
		'x': 0,
		'y': 3,
		'z': 0
	}
	
	assert letter_frequency(letter_count('./hw1/frost.txt')) == {
		'a': 0.06190476190476191, 
		'b': 0.009523809523809525, 
		'c': 0.02857142857142857, 
		'd': 0.047619047619047616, 
		'e': 0.10952380952380952, 
		'f': 0.05714285714285714, 
		'g': 0.009523809523809525, 
		'h': 0.05714285714285714, 
		'i': 0.10952380952380952, 
		'j': 0.0, 
		'k': 0.009523809523809525, 
		'l': 0.02857142857142857, 
		'm': 0.014285714285714285, 
		'n': 0.04285714285714286, 
		'o': 0.09523809523809523, 
		'p': 0.004761904761904762, 
		'q': 0.0, 
		'r': 0.06666666666666667, 
		's': 0.06666666666666667, 
		't': 0.09523809523809523, 
		'u': 0.023809523809523808, 
		'v': 0.009523809523809525, 
		'w': 0.0380952380952381, 
		'x': 0.0, 
		'y': 0.014285714285714285, 
		'z': 0.0
	}

if __name__ == "__main__": __run_tests()