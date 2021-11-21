from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

#Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, 
# then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #Each character is either a knight or a knave, but not both 
    Biconditional(AKnight,Not(AKnave)),
    #Knave lies
    Implication(AKnave, Not(And(AKnight,AKnave))),
    #Knight tells the truth 
    Implication(AKnight,And(AKnight,AKnave))
)
# Puzzle 1
# A says "We are both knaves." And(AKnave,BKnave)
# B says nothing.
knowledge1 = And(
    #Each character is either a knight or a knave, but not both 
    Biconditional(AKnight,Not(AKnave)),
    Biconditional(BKnight,Not(BKnave)),
     #Knave lies
    Implication(AKnave, Not(And(AKnave,BKnave))),
    #Knight tells the truth 
    Implication(AKnight,And(AKnave,BKnave))   
)
# Puzzle 2
# A says "We are the same kind."  Or(And(AKnave,BKnave),And(AKnight,BKnight))
# B says "We are of different kinds." Not
knowledge2 = And(
    #Each character is either a knight or a knave, but not both 
    Biconditional(AKnight,Not(AKnave)),
    Biconditional(BKnight,Not(BKnave)),
    #AKnave lies
    Implication(AKnave, Not(Or(And(AKnave,BKnave),And(AKnight,BKnight)))),
    #AKnight tells the truth 
    Implication(AKnight,Or(And(AKnave,BKnave),And(AKnight,BKnight))),
    #BKnave lies
    Implication(BKnave,Or(And(AKnave,BKnave),And(AKnight,BKnight))),
    #BKnight tells the truth 
    Implication(BKnight,Not(Or(And(AKnave,BKnave),And(AKnight,BKnight)))),
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. Or(AKnight,AKnave)
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."s
knowledge3 = And(
    #Each character is either 
    # a knight or a knave, but not both 
    Biconditional(AKnight,Not(AKnave)),
    Biconditional(BKnight,Not(BKnave)),
    Biconditional(CKnight,Not(CKnave)),
    #A says the truth
    Implication(AKnight,Or(AKnave,AKnight)),
    #A lies
    #BKnight says the truth
    Implication(BKnight,Implication(Or(AKnave,AKnight),BKnave)),
    #BNave lies
    #Implication(BKnave,Not(Implication(Or(AKnave,AKnight),BKnave))),
    #BKnight says the truth 
    Implication(BKnight,CKnave),
    #BNave lies
    Implication(BKnave,Not(CKnave)),
    #C says the truth
    Implication(CKnight,AKnight),
    #C lies
    Implication(CKnave,Not(AKnight))
)

knowledge5 = And(
    Biconditional(AKnight,Not(AKnave)),
    Biconditional(BKnight,Not(BKnave)),
    Biconditional(CKnight,Not(CKnave)),
    Not(AKnight)
)
print(model_check(knowledge5, AKnave))

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
