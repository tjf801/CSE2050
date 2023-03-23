import maze

# this starter code has successfully embodied literally everything i hate about programming. Thanks!

class Game():
    '''Holds the game solving logic. Initialize with a fully initialized maze'''
    
    def __init__(self, _maze):
        self._maze: maze.Maze = _maze
    
    # Creating simple methods (like the next two) to abstract core parts 
    #   of your algorithm helps increase the readability of your code.
    #   You will find these two useful in your solution.

    def _is_move_available(self, row, col, path):
        '''If (row, col) is already in the solved path then it is not available'''
        return (row, col) not in path \
            and self._maze.is_move_in_maze(row, col) and not self._maze.is_wall(row, col)

    def _is_puzzle_solved(self, row, col):
        '''Is the given row,col the finish square?'''
        return self._maze.get_finish() == (row, col)


    ########################################################
    def find_route(self, currow: int, curcol: int, curscore: int, curpath: list[tuple[int, int]]) -> tuple[int, list[tuple[int, int]]]:
        if self._maze.get_finish() == (currow, curcol):
            return curscore, curpath + [(currow, curcol)]
        
        score, path = max(
            [
                self.find_route(
                    currow + dx, curcol + dy, 
                    curscore, curpath + [(currow, curcol)]
                )
                for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))
                if self._is_move_available(currow + dx, curcol + dy, curpath)
            ] + [(-1, [])],
            key=lambda x: x[0]
        )
        
        assert self._maze._maze[currow][curcol] != '*'
        
        return score + self._maze._maze[currow][curcol], path # type: ignore



# This block of code will be useful in debugging your algorithm. But you still need
#  to create unittests to thoroughly testing your code.
if __name__ == '__main__':
    # Here is how you create the maze. Pass the row,col size of the grid.
    grid = maze.Maze(3, 3)
    # You have TWO options for initializing the Value and Walls squares.
    # (1) init_random() and add_random_walls()
    #     * Useful when developing your algorithm without having to create 
    #         different grids
    #     * But not easy to use in testcases because you cannot preditably
    #         know what the winning score and path will be each run
    # (2) _set_maze()
    #     * You have to create the grid manually, but very useful in testing
    #       (Please see the test_game.py file for an example of _set_maze())
    grid.init_random(0,9) # Initialze to a random board
    grid.add_random_walls(0.2)   # Make a certian percentage of the maze contain walls

    # AFTER you have used one of the two above methods of initializing 
    #   the Values and Walls, you must set the Start Finish locations. 
    start = (0,2)
    finish = (1,1)
    grid.set_start_finish(start, finish)

    # Printing the starting grid for reference will help you in debugging.
    print(grid)           # Print the maze for visual starting reference

    # Now instatiate your Game algorithm class
    game = Game(grid)     # Pass in the fully initialize maze grid
    
    # Now initiate your recursize solution to solve the game!
    # Start from the start row, col... zero score and empty winning path
    score, path = game.find_route(start[0], start[1], 0, list())
    print(f"The winning score is {score} with a path of {path}")
