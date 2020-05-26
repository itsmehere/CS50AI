# Knights and Knaves

[Knights and Knaves](https://en.wikipedia.org/wiki/Knights_and_Knaves) is a puzzle created by logician, 
[Raymond Smullyan](https://en.wikipedia.org/wiki/Raymond_Smullyan) in 1978 and was first introduced in 
his book titled,"What is the name of this book?"

In the puzzle, each character is either a knight or a knave. Knights always tell the truth and knaves always lie.

Example: Person A says: "I am both a knight and a knave."

If A were a knight, then we know that A is a knight AND a knave. However, we also know that this can't possibly be true
because A can only be one of the two. Thus, we can conclude that A is lying and must be a knave.

## Understanding

`logic.py`: Contains the implementation for the propositional connectives as well as the 
[model_checking](https://en.wikipedia.org/wiki/Model_checking#Symbolic_model_checking) algorithm.

`puzzle.py`: Contains the 4 different puzzles that the computer will solve.

## Usage

```python
python puzzle.py
```
