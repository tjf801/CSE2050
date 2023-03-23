from __future__ import annotations
import timeit
import typing

_T = typing.TypeVar('_T')

def time_function(func: typing.Callable[[_T], typing.Any], arg: _T, n_trials: int = 10) -> float:
    "Measure the time it takes to run a function on a given argument"
    t = timeit.timeit(lambda: func(arg), number=n_trials)
    return t / n_trials

if typing.TYPE_CHECKING: # only supported in python 3.11+
    _A = typing.TypeVarTuple('_A')

def time_function_flexible(func: 'typing.Callable[[typing.Unpack[_A]], typing.Any]', args: 'tuple[typing.Unpack[_A]]', n_trials: int = 10) -> float:
    "Measure the time it takes to run a function on given arguments"
    t = timeit.timeit(lambda: func(*args), number=n_trials)
    return t / n_trials


if __name__ == '__main__':
    # Some tests to see if time_function works
    def test_func(L: list[int]):
        for item in L:
            item *= 2
    
    L1 = [i for i in range(10**5)]
    t1 = time_function(test_func, L1)
    
    L2 = [i for i in range(10**6)] # should be 10x slower to operate on every item
    t2 = time_function(test_func, L2)
    
    print("t(L1) = {:.3g} ms".format(t1*1000))
    print("t(L2) = {:.3g} ms".format(t2*1000))