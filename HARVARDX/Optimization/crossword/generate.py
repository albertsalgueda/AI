import sys
import copy
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
        #every value in a variable’s domain has the same number of letters as the variable’s length.
        for var in self.crossword.variables:
            var_lenght = var.length
            for word in self.crossword.words:
                if len(word) != var.length:
                    self.domains[var].remove(word)
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #A conflict in the context of the crossword puzzle is a square for which two variables disagree on what character value it should take on.)
        overlap = self.crossword.overlaps[x][y]  
        # will return a tupple (i,j) ith positionn in x and jth position in y 
        i = overlap[0]
        j = overlap[1]
        if overlap is not None:
            for word1 in self.domains[x]:
                for word2 in self.domains[y]:
                    if word1[i] != word2[j]:
                        self.domains[x].remove(word1)
                        return True
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        starting = True
        my_arcs=[]
        #create the list of arcs 
        if arcs is None:
            for arc in self.crossword.variables:
                for arc2 in self.crossword.neighbours(arc):
                    if arc != arc2:
                        arcs.append(tuple(arc,arc2))
            starting = False
        if starting:
            queue = arcs
        else:
            queue = my_arcs 
            
        def DEQUEUE(queue):
            #can be implemented better
            return queue.pop()
        
        def ENQUEUE(queue,tupple):
            return queue.append(tupple)
        
        while queue is not None:
            (x,y) = DEQUEUE(queue) 
            if self.revise(x,y):
                if len(self.domains[x])== 0:
                    #nothing else to explore 
                    return False
                neighbours = copy.deepcopy(self.crossword.neighbours(x))
                if y in neighbours: 
                    neighbours = neighbours - {y}
                for z in neighbours:
                    queue =  ENQUEUE(queue,tuple(z,y))
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #every value is the correct length
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False
            elif assignment[var] not in self.crossword.words:
                return False
        #no conflicts between neighboring variables.
        #print(consistency)
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #assignment is a dictionary where the keys are Variable objects and the values are strings 
        # representing the words those variables will take on.
        for var in assignment:
            domain = assignment[var]
            #every value is the correct length
            if len(domain) != var.lenght:
                return False
            #all values are distinct, no overlaps
            for var2 in assignment:
                domain2 = assignment[var2]
                if domain == domain2:
                    return False
                overlap = self.crossword.overlaps[var,var2]
                if overlap is not None:
                    return False
         
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        possible_vars = []
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return var                
                
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if len(assignment) == len(self.crossword.variables):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new = assignment.copxy()
            new[var] = value
            if self.consistent(new):
                result = self.backtrack(new)
                if result is not None:
                    return result
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
