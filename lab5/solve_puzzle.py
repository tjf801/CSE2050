from __future__ import annotations
from functools import cache
from typing import Iterable


def solve_puzzle(board: Iterable[int]) -> bool:
	board = tuple(board)
	assert all(isinstance(x, int) and 0 <= x for x in board), "board must be a sequence of non-negative integers"
	return _solve_from_index(board, 0)

@cache
def _solve_from_index(board: tuple[int], index: int) -> bool:
	if index == len(board) - 1:
		return True
	
	# NOTE: since "You can assume the numbers on tiles are non-negative integers", 
	#       we can use -1 to signify that we have already visited this index
	if board[index] == -1:
		return False
	# NOTE: if we are at a zero and not finished, we are stuck
	elif board[index] == 0:
		return False
	
	clockwise_next_index = (index + board[index]) % len(board)
	counterclockwise_next_index = (index - board[index]) % len(board)
	
	# NOTE: we need to make a copy of the board, since we are mutating it
	# (yes i know there's technically a faster way to do this, but this way is more readable)
	new_board = list(board)
	new_board[index] = -1 # mark this index as visited
	new_board = tuple(new_board)
	
	return _solve_from_index(new_board, clockwise_next_index) \
		or _solve_from_index(new_board, counterclockwise_next_index)