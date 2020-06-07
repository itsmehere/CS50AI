from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Game Rules: Either AKnight or AKnave but not both.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A says:
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Game Rules: Either AKnight or AKnave but not both.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # Game Rules: Either BKnight or BKnave but not both.
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A Says:
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Game Rules: Either AKnight or AKnave but not both.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # Game Rules: Either BKnight or BKnave but not both.
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A: If A is telling the truth, then A is a Knight and A & B are of the same kind.
    Biconditional(Or(And(AKnight, BKnight), And(AKnave, BKnave)), AKnight),

    # B: If B is telling the truth, then B is a Knight and A & B are of different kinds.
    Biconditional(Or(And(AKnave, BKnight), And(AKnight, BKnave)), BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Game Rules: Either AKnight or AKnave but not both.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # Game Rules: Either BKnight or BKnave but not both.
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Game Rules: Either CKnight or CKnave but not both.
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A:
    Biconditional(AKnight, Or(AKnight, AKnave)),

    # B:
    Biconditional(AKnight, BKnave),
    Biconditional(BKnight, CKnave),

    # C:
    Biconditional(CKnight, AKnight)
)


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
