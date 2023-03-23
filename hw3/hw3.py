from __future__ import annotations
import timeit
import typing


def find_pairs_naive(nums: list[int], target: int) -> set[tuple[int, int]]:
	"Find all pairs of indices that sum to target"
	# assert len(set(nums)) == len(nums), "No duplicate entries allowed"
	
	pairs = set()
	for i, n in enumerate(nums):                 # iteration: O(n)
		for m in nums[i+1:]:                     # iteration: O(n)
			if n + m == target:                  # comparison: O(1)
				pairs.add((n, m))                # insertion: O(1)
	return pairs                                 # total: O(n) * ( O(n) * ( O(1) + O(1) ) ) = O(n^2)

def find_pairs_optimized(nums: typing.Iterable[int], target: int) -> set[tuple[int, int]]:
	"Find all pairs of indices that sum to target"
	# convert to list first because for some reason we need to return a
	# set[tuple[int, int]] instead of a set[set[int]], so we need to iterate
	# over the list in order
	nums = list(nums)                            # implicit iteration: O(n)
	
	num_set = set(nums)                          # iteration (again): O(n)
	pairs = set()
	
	for n in nums:                               # iteration: O(n)
		m = target - n                           # subtraction: O(1)
		if m in num_set and m != n:              # lookup + comparison: O(1)
			# make sure that we don't add the same pair twice
			if (m, n) not in pairs:              # lookup: O(1)
				pairs.add((n, m))                # insertion: O(1)
	
	return pairs                                 # total: O(n) + O(n) + O(n) * ( O(1) + O(1) + O(1) ) = O(n)


if typing.TYPE_CHECKING:
	import sys
	if sys.version_info >= (3, 11):
		_A = typing.TypeVarTuple("_A")

def measure_min_time(fn: typing.Callable[[typing.Unpack[_A]], typing.Any], args: tuple[typing.Unpack[_A]], num_trials: int = 10) -> float:
	"Measure the minimum time taken to run a function"
	return min(timeit.repeat(lambda: fn(*args), number=1, repeat=num_trials))

def main():
	print("  n  |  naive  | optimized")
	print("-----+---------+-----------")
	for n in [10, 50, *range(100, 1100, 100)] + [2000, 5000]:
		nums = list(range(n))
		target = n + 1
		
		naive_time = measure_min_time(find_pairs_naive, (nums, target))
		optimized_time = measure_min_time(find_pairs_optimized, (nums, target))
		
		print(f"{n:4d} | {naive_time:7.5f} | {optimized_time:9.7f}")

if __name__ == "__main__": main()