# type: ignore

import random
from typing import Literal, TypeAlias, Union

# DO NOT modify any code in this class!
#    I wouldnt, but this shit is so bad I cant help myself.
#    Like you literally have a function called _print_maze that doesnt print the maze
#    Also you have default args that are mutable
#    And u literally seem allergic to any form of type hints
#    And also you keep intitializing instance variables in completely random places
#    Like.. I thought u were a java dev?? Doesnt java just not compile unless you initialize ur variables?
#    Actually wait i think it initializes them to null by default unless theyre `final``. Also now that im 
#    thinking abt it, iirc u were actually a Go dev. So it's probably *encouraged* to 
#    initialize things in random places.

#    TL;DR: this is why I hate the average python developer.

#    UPDATE: even AFTER adding type hints, this file still has EIGHT errors vs code is complaining about.

WallChar: TypeAlias = Literal['*']

class Maze():
    '''The actual grid of the maze that we are trying to solve.'''
    MINVAL = 0 # default
    MAXVAL = 9 # default
    WALL_CHAR: WallChar = "*"
    
    _maze: Union[list[list[int]], list[list[Union[int, WallChar]]]] # this is so bad
    _rows: int
    _cols: int
    _minval: int
    _maxval: int
    _start: tuple[int, int]
    _finish: tuple[int, int]
    
    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._minval = Maze.MINVAL
        self._maxval = Maze.MAXVAL
    
    # Testing method - the 2D list representing the maze can be set externally to facilitate testing
    # see, i dont even know what type of list this is supposed to be. I'm literally just guessing here.
    def _set_maze(self, lst: list[list[Union[int, WallChar]]]):
        self._maze = lst
    
    def init_random(self, minval: int = MINVAL, maxval: int = MAXVAL):
        '''Initialize with random values. Optionally pass the min and max values for point values.'''
        # 2D array:  rows,cols
        self._maze = [[random.randrange(minval, maxval) for _ in range(self._rows)] for _ in range(self._cols)]
        self._minval = minval
        self._maxval = maxval
    
    def add_random_walls(self, percent_obstruction: float):
        '''Insert some random "walls" to make the maze non-trivial. The
        percent_obstruction (float in 0..1) determines the frequency of the walls in the
        maze. The more walls, the less winning paths and the less
        recursion will be needed for the solution. But it also means
        that some mazes will have no possible path from Start to Finish.'''
        
        threshold = int((self._maxval - self._minval) * percent_obstruction)
        for row in range(self._rows):
            for col in range(self._cols):
                # shit like this is why we use type hints...
                # if this method is called more than once on the same maze object, it crashes.
                # using only unit tests without type checking really works WONDERS.
                if self._maze[row][col] < threshold: # type: ignore
                    # Add wall to this row,col
                    self._maze[row][col] = self.WALL_CHAR # type: ignore
    
    def __repr__(self) -> str:
        return self._print_maze()
    
    # so much for "no mutable default args" LOL
    # VS code is literally giving me a warning about this.
    # also, this function literally does not even print the maze!!! wtf???
    def _print_maze(self, winningpath: list[tuple[int, int]] = list()) -> str:
        '''Prints out the grid with values, walls, start and finish squares.
        Optionally pass the winning list/path of tuples if you want the winning route
        to be show as '@' characters.'''
        # NOTE: yes, i know that here, the winningpath isnt ever modified, but its still ABYSMAL that 
        #       one would even do this. its LITERALLY less work to type out an empty tuple, or if you 
        #       feel like a whopping thirty or so extra keystrokes, just using None as the default. AAAA
        result = "    "
        for col in range(self._cols):
            # Add the column headers
            result += f" {col} "
        result += "\n"
        for row in range(self._rows):
            result += f"\n{row}   " # Add the row header
            for col in range(self._cols):
                if (row, col) == self._start:
                    result += " S "  # Start square
                elif (row, col) == self._finish:
                    result += " F "  # Finish square
                elif (row, col) in winningpath:
                    result += " @ "  # Square in winning path
                else:
                    result += f" {self._maze[row][col]} "  # Value square
        return result + "\n"
    
    def is_move_in_maze(self, row: int, col: int) -> bool:
        '''Checks if the potential move is in the maze'''
        return row >= 0 and row < self._rows and col >= 0 and col < self._cols
    
    def is_wall(self, row: int, col: int) -> bool:
        '''Is the given location a wall'''
        return self._maze[row][col] == self.WALL_CHAR

    def make_move(self, row: int, col: int, path: list[tuple[int, int]]) -> int:
        '''Make the given move. Add the row,col to the path and
        return the value.'''
        path.append((row,col))
        # there are literally no checks here. what if the move is out of bounds? or a wall???
        return self._maze[row][col] # type: ignore
    
    def set_start_finish(self, start, finish):
        '''Set the start and finish squares in the maze'''
        # raise sensible exception types challenge (2023) (IMPOSSIBLE DIFFICULTY) (99% FAIL!) (GONE WRONG) 😱😱😱
        if not self.is_move_in_maze(start[0], start[1]) or not self.is_move_in_maze(start[0], start[1]):
            raise RuntimeError("Start and Finish must be in the maze")
        if start == finish:
            raise RuntimeError("Start and Finish must be different locations")
        # me when Pylance(reportUninitializedInstanceVariable)
        self._start: tuple[int, int] = start
        self._finish: tuple[int, int] = finish
        # Set the start and finish to 0 values
        self._maze[start[0]][start[1]] = 0
        self._maze[finish[0]][finish[1]] = 0
    
    def get_start(self) -> tuple[int, int]:
        '''Get the starting square as a tuple'''
        # if you havent run set_start_finish yet, this will crash.
        # also, why is this a method? why not just make it a property?
        # ALSO also, why tf isnt there even ANY documentation for this method???
        # like the entire point of having docstrings is to actually... DOCUMENT THE METHOD?? but no!!! 
        # saying "you must run set_start_finish first" is too much work. Instead you just let the user 
        # figure it out themselves, and stick to the docstring that literally could be generated by 
        # a literal AI and provides no acutal help to the programmer!!! (I am going insane)
        return self._start
    
    def get_finish(self) -> tuple[int, int]:
        '''Get the finish square as a tuple'''
        # see above.
        return self._finish
