import sys
import copy
from crossword import Variable,Crossword

# python generate.py data/structure0.txt data/words0.txt 

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
        #make a deep copy
        domain_copy = copy.deepcopy(self.domains)
        #every value in a variable’s domain has the same number of letters as the variable’s length.
        for var in domain_copy:
            for word in domain_copy[var]:
                if len(word) != var.length:
                    #if the lenght of the word is not the same of the required variable delete it 
                    self.domains[var].remove(word)
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        #A conflict in the context of the crossword puzzle is a square for which two variables disagree on what character value it should take on.)
        overlap = self.crossword.overlaps[x,y]  
        # will return a tupple (i,j) ith positionn in x and jth position in y 
        i = overlap[0]
        j = overlap[1]
        #make a deep copy 
        domains_copy = copy.deepcopy(self.domains)
        if overlap is not None:
            for wordX in domains_copy[x]:
                match = False
                for wordY in domains_copy[y]:
                    #if both words have the same letter in overlapping positions:
                    if wordX[i] == wordY[j]:
                        match = True #match found, no need to look for other words
                        break
                if match:
                    continue
                else:
                    revision = True
                    self.domains[x].remove(wordX) #if the word doesn't match any, remove it 
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #create the list of arcs 
        if not arcs:
            # no arcs provided, start with an initial queue of all of the arcs in the problem
            queue = []
            # populating queue
            for variable1 in self.domains:
                for variable2 in self.crossword.neighbors(variable1):
                    if self.crossword.overlaps[variable1, variable2] is not None:
                        queue.append((variable1, variable2))

        while len(queue) > 0:
            #while there are items in the list
            #take an item to the list 
            i, j = queue.pop(0)
            if self.revise(i, j):
                #if the domain is empty return false 
                if len(self.domains[i]) == 0:
                    return False
                #check out the neighbours and add next item to the list 
                for neighbour in self.crossword.neighbors(i):
                    if neighbour != j:
                        queue.append((neighbour, i))
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

        # all values are distinct
        words = [*assignment.values()]
        if len(words) != len(set(words)):
            return False

        # every value is the correct length
        for variable in assignment:
            if variable.length != len(assignment[variable]):
                return False

        # there are no conflicts
        for variable in assignment:
            for neighbour in self.crossword.neighbors(variable):
                if neighbour in assignment:
                    i, j = self.crossword.overlaps[variable, neighbour]
                    if assignment[variable][i] != assignment[neighbour][j]:
                        return False

        #return True after it has passed all checks
        return True

    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_dict = {}
        neighbours = self.crossword.neighbors(var)

        # iterate through variable's words
        for word in self.domains[var]:
            eliminated = 0
            for neighbour in neighbours:
                # don't count if neighbor has already assigned value
                if neighbour in assignment:
                    continue
                else:
                    # calculate overlap between two variables
                    overlap = self.crossword.overlaps[var,neighbour]  
                    # will return a tupple (i,j) ith positionn in x and jth position in y 
                    i = overlap[0]
                    j = overlap[1]
                    for neighbour_word in self.domains[neighbour]:
                        # iterate through neighbour's words, check for eliminate ones
                        if word[i] != neighbour_word[j]:
                            eliminated += 1
            # add eliminated neighbour's words to temporary dict
            word_dict[word] = eliminated

        # sorting..
        sorted_dict = {k: v for k, v in sorted(word_dict.items(), key=lambda item: item[1])}

        return [*sorted_dict]

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
        #get an unassigned variable
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new = assignment.copy()
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
