import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP  | NP VP Conj NP VP
AdjP -> Adj | Adj N PP | Adj AdjP
NP -> N | N PP | Det N | Det N PP | Det AdjP N | Det N Adv | Det AdjP
PP -> P NP
VP -> V | V NP | V PP | Adv V NP | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize lower-cased sentence
    tokenized = nltk.word_tokenize(sentence.lower())
    
    # Remove any word that has no alphabetical character
    for word in tokenized:
        if not any(c.isalpha() for c in word):
            tokenized.remove(word)
            
    return tokenized


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    npChunks = []

    for part in tree:
        if part.label() == "NP":
            # Get a list of the subtrees and remove the current tree
            subtrees = list(part.subtrees())
            subtrees.remove(part)
            
            # If the current NP tree contains no NP's, add to the list
            if not containsNP(subtrees):
                npChunks.append(part)
        else:
            # If the current tree isn't an NP tree, recursively call np_chunk
            if part.height() > 2:
                npChunks.extend(np_chunk(part))

    return npChunks

# Checks to see if a current tree has NP's underneath it
def containsNP(subtrees):
    for s in subtrees:
        if s.label() == "NP":
            return True

    return False

if __name__ == "__main__":
    main()
