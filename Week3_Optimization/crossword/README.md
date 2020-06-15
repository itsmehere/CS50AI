# Crossword

An AI to generate crossword puzzles.

## Background:

How might you go about generating a crossword puzzle? Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. We can model this sort of problem as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence). Consider the following crossword puzzle structure.

![crossword](https://cs50.harvard.edu/ai/2020/projects/3/crossword/images/structure.png)

In this structure, we have four variables, representing the four words we need to fill into this crossword puzzle (each indicated by a number in the above image). Each variable is defined by four values: the row it begins on (its `i` value), the column it begins on (its `j` value), the direction of the word (either down or across), and the length of the word. Variable 1, for example, would be a variable represented by a row of `1` (assuming `0` indexed counting from the top), a column of `1` (also assuming `0` indexed counting from the left), a direction of `across`, and a length of `4`.

As with many constraint satisfaction problems, these variables have both unary and binary constraints. The unary constraint on a variable is given by its length. For Variable 1, for instance, the value `BYTE` would satisfy the unary constraint, but the value `BIT` would not (it has the wrong number of letters). Any values that don’t satisfy a variable’s unary constraints can therefore be removed from the variable’s domain immediately.

The binary constraints on a variable are given by its overlap with neighboring variables. Variable 1 has a single neighbor: Variable 2. Variable 2 has two neighbors: Variable 1 and Variable 3. For each pair of neighboring variables, those variables share an overlap: a single square that is common to them both. We can represent that overlap as the character index in each variable’s word that must be the same character. For example, the overlap between Variable 1 and Variable 2 might be represented as the pair `(1, 0)`, meaning that Variable 1’s character at index 1 necessarily must be the same as Variable 2’s character at index 0 (assuming 0-indexing, again). The overlap between Variable 2 and Variable 3 would therefore be represented as the pair `(3, 1)`: character 3 of Variable 2’s value must be the same as character 1 of Variable 3’s value.

For this problem, we’ll add the additional constraint that all words must be different: the same word should not be repeated multiple times in the puzzle.

## Understanding:

There are two Python files in this project: `crossword.py` and `generate.py`. The first has been entirely written for you, the second has some functions that are left for you to implement.

First, let’s take a look at `crossword.py`. This file defines two classes, `Variable` (to represent a variable in a crossword puzzle) and `Crossword` (to represent the puzzle itself).

Notice that to create a `Variable`, we must specify four values: its row `i`, its column `j`, its direction (either the constant `Variable.ACROSS` or the constant `Variable.DOWN`), and its length.

The `Crossword` class requires two values to create a new crossword puzzle: a `structure_file` that defines the structure of the puzzle (the _ is used to represent blank cells, any other character represents cells that won’t be filled in) and a `words_file` that defines a list of words (one on each line) to use for the vocabulary of the puzzle. Three examples of each of these files can be found in the `data` directory of the project, and you’re welcome to create your own as well.

Note in particular, that for any crossword object `crossword`, we store the following values:

`crossword.height` is an integer representing the height of the crossword puzzle.  
`crossword.width` is an integer representing the width of the crossword puzzle.  
`crossword.structure` is a 2D list representing the structure of the puzzle. For any valid row `i` and column `j`, `crossword.structure[i][j]` will be `True` if the cell is blank (a character must be filled there) and will be `False` otherwise (no character is to be filled in that cell).  
`crossword.words` is a set of all of the words to draw from when constructing the crossword puzzle.  
`crossword.variables` is a set of all of the variables in the puzzle (each is a Variable object).  
`crossword.overlaps` is a dictionary mapping a pair of variables to their overlap. For any two distinct variables `v1` and `v2`, `crossword.overlaps[v1, v2]` will be `None` if the two variables have no overlap, and will be a pair of integers `(i, j)` if the variables do overlap. The pair `(i, j)` should be interpreted to mean that the `ith` character of `v1`’s value must be the same as the `j`th character of `v2`’s value.

Crossword objects also support a method `neighbors` that returns all of the variables that overlap with a given variable. That is to say, `crossword.neighbors(v1)` will return a set of all of the variables that are neighbors to the variable `v1`.

Next, take a look at `generate.py`. Here, we define a class `CrosswordCreator` that we’ll use to solve the crossword puzzle. When a `CrosswordCreator` object is created, it gets a `crossword` property that should be a `Crossword` object (and therefore has all of the properties described above). Each `CrosswordCreator` object also gets a `domains` property: a dictionary that maps variables to a set of possible words the variable might take on as a value. Initially, this set of words is all of the words in our vocabulary, but we’ll soon write functions to restrict these domains.

## Usage:

To run using `structure0` and `words0`:
```
python generate.py data/structure0.txt data/words0.txt
```

## My Output:

With heuristics:
```
C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure0.txt data/words0.txt
█SIX█
█E██F
█V██I
█E██V
█NINE

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure0.txt data/words1.txt
█BIT█
█A██B
█Y██Y
█E██T
█SINE

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure0.txt data/words2.txt
█SIT█
█A██P
█L██I
█E██P
█SAFE

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure1.txt data/words0.txt
No solution.

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure1.txt data/words1.txt
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure1.txt data/words2.txt
██████████████
███████L████R█
█SIGNIFICANCE█
█C█████C████C█
█A██AFTER███R█
█L█████N████U█
█E███RESULT█I█
███████E████T█
██████████████

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure2.txt data/words0.txt
No solution.

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure2.txt data/words1.txt
██████C
LOSS██R
I██TRUE
N██A██A
E██R██T
█BIT██E

C:\Users\mihir\Programming\CS50AI\Week3_Optimization\crossword>python generate.py data/structure2.txt data/words2.txt
██████C
PIPE██R
A██LAKE
I██I██D
R██T██I
█USE██T
```

## Other Links:

Read more about cs50ai [here](https://cs50.harvard.edu/ai/2020/)  
[Original Problem Page](https://cs50.harvard.edu/ai/2020/projects/3/crossword/)