Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import nltk
... import sys
... 
... TERMINALS = """
... Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
... Adv -> "down" | "here" | "never"
... Conj -> "and" | "until"
... Det -> "a" | "an" | "his" | "my" | "the"
... N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
... N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
... N -> "smile" | "thursday" | "walk" | "we" | "word"
... P -> "at" | "before" | "in" | "of" | "on" | "to"
... V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
... V -> "smiled" | "tell" | "were"
... """
... 
... NONTERMINALS = """
... S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
... 
... NP -> N | Det N | Det AP N | P NP | NP P NP
... VP -> V | Adv VP | V Adv | VP NP | V NP Adv
... PP -> P NP
... AP -> Adj | AP Adj
... """
... 
... grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
... parser = nltk.ChartParser(grammar)
... 
... 
... def main():
... 
...     # If filename specified, read sentence from file
...     if len(sys.argv) == 2:
...         with open(sys.argv[1]) as f:
...             s = f.read()
... 
...     # Otherwise, get sentence as input
...     else:
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
    # Tokenize the sentence and turn it into lowercase
    words = nltk.word_tokenize(sentence.lower())

    # Exclude any word that doesn’t contain at least one alphabetic character
    for word in words:
        flag = False
        if any(letter.isalpha() for letter in word):
            flag = True
        if not flag:
            words.remove(word)

    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    parent_tree = nltk.tree.ParentedTree.convert(tree)

    for subtree in parent_tree.subtrees():
            if subtree.label() == "N":
                np_chunks.append(subtree.parent())

    return np_chunks

if __name__ == "__main__":
