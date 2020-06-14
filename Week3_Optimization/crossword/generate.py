import sys
import copy
import math

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            varsToRemove = set()
            for value in self.domains[variable]:
                # If the variable length and the length of the word aren't equal, remove
                # the word from the domain of the variable - unary constraint
                if len(value) != variable.length:
                    varsToRemove.add(value)
            for var in varsToRemove:
                self.domains[variable].remove(var)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False

        valuesToRemove = set()
        revised = False

        for xVal in self.domains[x]:
            foundPossibleVal = False
            for yVal in self.domains[y]:
                # If the letters at the given overlap point are equal, it is a possible value 
                if xVal[overlap[0]] == yVal[overlap[1]] and xVal != yVal:
                    foundPossibleVal = True
                    break
            # If you didn't find a possible value: yVal, then that particular value: xVal won't work
            if foundPossibleVal == False:
                valuesToRemove.add(xVal)
                revised = True

        # Remove all values from x's domain that won't work for y
        for value in valuesToRemove:
            self.domains[x].remove(value)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        pairsToProcess = set()

        if arcs is None:
            for varA in self.crossword.variables:
                for varB in self.crossword.neighbors(varA):
                    pairsToProcess.add((varA, varB))
        else:
            pairsToProcess = arcs

        while len(pairsToProcess) != 0:
            pair = pairsToProcess.pop()

            # Check if the first variable in pair was revised to be arc-consistent
            if self.revise(pair[0], pair[1]):
                if len(self.domains[pair[0]]) == 0:
                    return False
                # Since the first var in pair was revised, make sure the neighbors of that variable are still arc-consistent
                for neighbor in self.crossword.neighbors(pair[0]):
                    pairsToProcess.add((neighbor, pair[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Make sure all variables are in the assignment
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for xVar in assignment:
            # Make sure the word's length and the variables length match
            if xVar.length != len(assignment[xVar]):
                return False

            for yVar in assignment:
                if xVar != yVar:
                    # Make sure no variables are assigned to the same value
                    if assignment[xVar] == assignment[yVar]:
                        return False
                    
                    overlap = self.crossword.overlaps[xVar, yVar]
                    if overlap == None:
                        continue

                    # Make sure characters of the word at overlap(if it exists) are the same
                    if assignment[xVar][overlap[0]] != assignment[yVar][overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Temporary
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        optimalVar = []
        minLength = math.inf

        for var in self.crossword.variables:
            # If the value isn't already in the assignment
            if var not in assignment.keys():

                # If the variable's domain length is shorter than the current variable's domain length, update optimalVar
                if len(self.domains[var]) < minLength:
                    minLength = len(self.domains[var])
                    optimalVar = var

                # If they are equal, choose the optimalVar based on number of neighbors
                elif len(self.domains[var]) == minLength:
                    if len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(optimalVar)):
                        minLength = len(self.domains[var])
                        optimalVar = var

        return optimalVar                

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        else:
            var = self.select_unassigned_variable(assignment)
            
            # Choose a variable to start and loop through the possible domain values of that variable
            for value in self.order_domain_values(var, assignment):
                assignment[var] = value

                # Make sure the assignment with the new value doesn't cause a contradiction
                if self.consistent(assignment):

                    # If it doesn't, continue the backtrack process with the new assignment
                    result = self.backtrack(assignment)

                    # If result is successful, return that result. Otherwise, the variable can't be assigned
                    # to the current value so continue testing more values in var's domain
                    if result != None:
                        return result
                    assignment[var] = None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
