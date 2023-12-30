import sys

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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        print(self.backtrack(dict()))
        return self.backtrack(dict())
    

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for domain in self.domains.keys():
            removeWord = []
            for word in self.domains[domain]:
                if domain.length != len(word):
                    removeWord.append(word)
            for word in removeWord:
                self.domains[domain].remove(word)
                
                
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        
        if overlap is None:
            return False
        else:
            to_remove = []
            for valX in self.domains[x]:
                for valY in self.domains[y]:
                    if valX[overlap[0]] == valY[overlap[1]]:
                        break
                else:
                    to_remove.append(valX)
                    revised = True
            
            for i in to_remove:
                self.domains[x].remove(i)
             
            return revised
            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        if arcs == None:
            for i in self.domains.keys():
                for j in self.domains.keys():
                    if i != j:
                        queue.append((i, j))
        else:
            for arc in arcs:
                queue.append(arc)
        
        while queue != None:
            arc = self.dequeue(queue)
            if arc is not None:
                x = arc[0]
                y = arc[1]
                if self.revise(x, y):
                    if len(self.domains[x]) == 0:
                        return False
                    for z in self.crossword.neighbors(x):
                        if z != y:
                            queue.append((z, x))
            else:
                break               
        return True
    
              
    def dequeue(self, queue):
        if queue:
            return queue.pop(0)
        else:
            return None        
    
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for val in self.domains.keys():
            if val not in assignment.keys():
                return False
            elif assignment[val] is None:
                return False
            
        return True
    

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        vals = []
        for key, value in assignment.items():
            if value in vals:
                return False
            else:
                vals.append(value)
                
            if key.length != len(value):
                return False
            
            neighbors_vals = self.crossword.neighbors(key)
            for neighbor in neighbors_vals:
                overlap = self.crossword.overlaps[key, neighbor]
                if neighbor in assignment:
                    if value[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
                    
        return True  
    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        vals = {}
        variables = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        
        for variable in variables:
            if variable in assignment:
                continue
            else:
                counter = 0
                for neighbor in neighbors:
                    if variable in self.domains[neighbor]:
                        counter += 1
                vals[variable] = counter
                
        return sorted(vals, key=lambda key: vals[key])     
       

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        values = 10000
        degrees = 0
        
        for var in self.domains.keys():
            if var in assignment:
                continue
            else:
                if values > len(self.domains[var]):
                    values = len(self.domains[var])
                    degrees = len(self.crossword.neighbors(var))
                    variable = var
                elif values == len(self.domains[var]):
                    if self.crossword.neighbors(var) is not None:
                        if degrees < len(self.crossword.neighbors(var)):
                            values = len(self.domains[var])
                            degrees = len(self.crossword.neighbors(var))
                            variable = var
                        else:
                            variable = var
                            value = len(self.domains[var])
                            degrees = 0
                            
        return variable
        

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
            for value in self.order_domain_values(var, assignment):
                assignment[var] = value
                if self.consistent(assignment):
                    answer = self.backtrack(assignment)
                    if answer is not None:
                        return answer
                assignment.pop(var)
                
        return None


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
