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
        known_mines = set()
        
        if self.cells == self.count and self.count > 0:
            known_mines = self.cells
            return known_mines
        
        return known_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        known_safes = set()
        
        if self.count == 0:
            known_safes = self.cells
            return known_safes

        return known_safes

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
            
    def knowledge_pieces(self, seq, size):
        """
        Extracts an array of 2 sentences from the knowledge base.
        """
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
        
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
        # Step 1
        self.moves_made.add(cell)
        
        # Step 2
        self.mark_safe(cell)
        
        # Step 3
        neighboring_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                
                # Ignore cell itself
                if (i, j) == cell:
                    continue
                
                # Ignore if it's a known mine
                if (i, j) in self.mines:
                    count -= 1
                    continue
                
                # Ignore if it's a known safe
                if (i, j) in self.safes:
                    continue
                
                # Ignore if it's a already moved
                if (i, j) in self.moves_made:
                    continue
                
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighboring_cells.add((i, j))
                
        new_sentence = Sentence(neighboring_cells, count)
        
        new_safe_cells = new_sentence.cells
        new_safe_cells_copy = new_sentence.cells.copy()
        
        if new_sentence.count == 0:
            for cell in new_safe_cells_copy:
                self.mark_safe(cell)
        elif new_sentence.count == 1 and len(new_sentence.cells) == 1:
            self.mark_mine(list(new_sentence.cells)[0])
        else:
            self.knowledge.append(new_sentence)
            
        # Step 4
        for sentence in self.knowledge:
            safe_cells = sentence.known_safes()
            safe_cells_copy = safe_cells.copy()
            
            if safe_cells_copy != set():
                pass
            
            if safe_cells:
                for cell in safe_cells_copy:
                    self.mark_safe(cell)
                    
            mines_cells = sentence.known_mines()
            mines_cells_copy = mines_cells.copy()
            
            if mines_cells != set():
                pass
            
            if mines_cells:
                for mine in mines_cells_copy:
                    self.mark_mine(mine)
            
        # Step 5
        new_knowledge = []
        
        if self.knowledge is not []:
            for sentences in self.knowledge_pieces(self.knowledge, 2):
                if len(sentences) > 1:
                    set1 = sentences[0]
                    set1_cells = set1.cells 
                    set1_count = set1.count
                    
                    set2 = sentences[1]
                    set2_cells = set2.cells 
                    set2_count = set2.count

                    if set1 == set2:
                        self.knowledge.remove(set2)
                    elif set1_cells != set2_cells:
                        if set1_cells.issubset(set2_cells):
                            new_cells = set2_cells - set1_cells
                            new_count = set2_count - set1_count
                            new_sentence = Sentence(new_cells, new_count)
                            new_knowledge.append(new_sentence)
                            
                        elif set2_cells.issubset(set1_cells):
                            new_cells = set1_cells - set2_cells
                            new_count = set1_count - set2_count
                            new_sentence = Sentence(new_cells, new_count)
                            new_knowledge.append(new_sentence)
                            
        if not new_knowledge:
            pass
        else:
            for new in new_knowledge:
                if new not in self.knowledge:
                    self.knowledge.append(new)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes.copy()
        
        safe_moves -= self.moves_made

        if len(safe_moves) == 0:
            return None
        
        move = safe_moves.pop()
        return move
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = set()

        i = random.randrange(self.height)
        j = random.randrange(self.width)
        random_move = (i, j)

        if random_move not in self.moves_made and random_move not in self.mines:
            random_moves.add(random_move)
        
        if len(random_moves) == 0:
            return None 

        random_move = random_moves.pop() 
        return random_move 
