import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # Add the cell to moves_made and mark it as a safe sell.
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Get a set of the surrounding cells and subtract the cells whose state we already know.
        listOfNeighbors = self.surroundingCells(cell) - self.safes - self.moves_made
        self.knowledge.append(Sentence(listOfNeighbors, count))

        # Mark new cells as safe or mines.
        inferedSafes = set()
        inferedMines = set()

        for sentence in self.knowledge:
            if len(sentence.cells) != 0:
                sentenceKnownSafes = sentence.known_safes()
                sentenceKnownMines = sentence.known_mines()

                inferedMines = inferedMines.union(sentenceKnownMines)
                inferedSafes = inferedSafes.union(sentenceKnownSafes)
            else:
                self.knowledge.remove(sentence)

        for safeCell in inferedSafes:
            self.mark_safe(safeCell)

        for mineCell in inferedMines:
            self.mark_mine(mineCell)


        # Edit sentences based on new inferences.
        for sentence1 in self.knowledge:
            # If empty, remove sentence. Otherwise, continue.
            if len(sentence1.cells) != 0:  
                for sentence2 in self.knowledge:
                    # If empty, remove sentence. Otherwise, continue.
                    if len(sentence2.cells) != 0:
                        # Update sentence2 with new inferences
                        if sentence1.cells.issubset(sentence2.cells) and sentence1 != sentence2:
                            sentence2.cells -= sentence1.cells
                            sentence2.count -= sentence1.count
                    else:
                        self.knowledge.remove(sentence2)
            else:
                self.knowledge.remove(sentence1)


    def surroundingCells(self, cell):
        """
        Returns all the surroundCells given a location.
        Given cell X, surroundingCells returns:
        C C C
        C X C
        C C C
        A set of all C's.
        """
        cells = set()

        # Use max and min to make sure this function returns the right values for corners
        # Loop through rows
        for i in range(max(0, cell[0] - 1), min(self.height, cell[0] + 2)):
            # Loop through columns
            for j in range(max(0, cell[1] - 1), min(self.width, cell[1] + 2)):
                # If the current cell is not the same as the selected cell, add to cells set.
                if (i, j) != (cell[0], cell[1]):
                    cells.add((i,j))  

        return cells    

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safeCell in self.safes:
            if safeCell not in self.moves_made:
                print(safeCell)
                return safeCell
        
        return None

        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        randCell = self.getRandomCell()
        blockedLocations = self.mines.union(self.moves_made)
        numIterations = 1

        while randCell in blockedLocations:
            if numIterations == len(blockedLocations):
                return None
            else:
                randCell = self.getRandomCell()
                numIterations += 1

        print(randCell)
        return randCell

    def getRandomCell(self):
        cell = (random.randint(0, self.height - 1), 
                random.randint(0, self.width - 1))
        return cell
        

