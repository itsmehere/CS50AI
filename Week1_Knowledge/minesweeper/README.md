# Minesweeper

Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

In this 3x3 Minesweeper game, for example, the three `1` values indicate that each of those cells has one neighboring cell that is a mine. The four `0` values indicate that each of those cells has no neighboring mine.

![minesweeperBoard](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/images/safe_cells.png)

The goal of Minesweeper is to uncover all the squares on a grid that do not contain mines without being "blown up" by clicking on a square with a mine underneath.

## Getting Started

- Once in the directory for the project, run `pip3 install -r requirements.txt` to install the required Python package (`pygame`) for this project if not already have it installed.

## Understanding

There are two main files in this project: `runner.py` and `minesweeper.py`. `minesweeper.py` contains all of the logic the game itself and for the AI to play the game. `runner.py` contains all of the code to run the graphical interface for the game.

## Usage

Simply run `python runner.py`

## More Info

If you want to learn more about CS50AI or this project in particular, head over to Harvard's CS50AI Pset: [Minesweeper](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/)

## NOTE

Minesweeper is a game that is built with some luck. When the AI is run (by clicking “AI Move”), note that it will not always win. There will be some cases where the AI must guess, because it lacks sufficient information to make a safe move. This is to be expected. `runner.py` will print whether the AI is making a move it believes to be safe or whether it is making a random move.