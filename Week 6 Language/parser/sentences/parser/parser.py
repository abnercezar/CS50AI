import nltk
import sys
import re

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
S -> N V
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
    Converta `sentença` em uma lista de suas palavras.
    Pré-processe a frase convertendo todos os caracteres em letras minúsculas
    e remover qualquer palavra que não contenha pelo menos uma letra alfabética
    personagem.
    """
    regex_pattern = re.compile(".*[a-z].*")

    words = nltk.word_tokenize(sentence.lower())
    words = [word for word in words if regex_pattern.match(word)]

    return words


def np_chunk(tree):
    """
    Retorna uma lista de todos os pedaços de sintagmas nominais na árvore de frases.
    Um pedaço de sintagma nominal é definido como qualquer subárvore da frase
    cujo rótulo é "NP" que não contém nenhum outro
    sintagmas nominais como subárvores.
    """
    np_chunks = []
    parented_tree = nltk.tree.ParentedTree.convert(tree)

    for subtree in parented_tree.subtrees(lambda t: t.label() == 'N'):
        np_chunks.append(subtree.parent())

    return np_chunks


if __name__ == "__main__":
    nltk.download('punkt')
    main()
