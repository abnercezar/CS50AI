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
S -> NP VP | S Conj S
NP -> Det N | Det Adj N | N | NP PP | NP Conj NP | Adj N | Det Adj N
VP -> V | V NP | V NP PP | V PP | VP Conj VP | Adv V | V Adv | VP NP
PP -> P NP
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
    # Compila um padrão regex que corresponde a qualquer
    # string que contenha pelo menos uma letra minúscula
    regex_pattern = re.compile(".*[a-z].*")

    # Tokeniza a frase em palavras e converte
    # todas as palavras para minúsculas
    words = nltk.word_tokenize(sentence.lower())

    # Filtra as palavras para incluir apenas
    # aquelas que correspondem ao padrão regex
    words = [word for word in words if regex_pattern.match(word)]

    # Retorna a lista de palavras
    return words


def np_chunk(tree):
    """
    Retorna uma lista de todos os pedaços de sintagmas nominais na árvore de frases.
    Um pedaço de sintagma nominal é definido como qualquer subárvore da frase
    cujo rótulo é "NP" que não contém nenhum outro
    sintagmas nominais como subárvores.
    """
    # Inicializa uma lista vazia para
    # armazenar os chunks de frase nominal (NP)
    np_chunks=[]

    # Para cada subárvore na árvore que é uma frase nominal (NP)
    for s in tree.subtrees(lambda t: t.label()=="NP"):

        # Inicializa um contador
        m=0

        # Para cada subárvore dentro da
        # subárvore atual que é uma frase nominal (NP)
        for i in s.subtrees(lambda t: t.label()=="NP"):

            # Incrementa o contador
            m+=1
        # Se o contador é igual a 1, ou seja, se a subárvore
        # atual não contém outras frases nominais (NP)
        if m==1:

            # Adiciona a subárvore à lista de
            # chunks de frase nominal (NP)
            np_chunks.append(s)

    # Retorna a lista de chunks de frase nominal (NP)
    return np_chunks


if __name__ == "__main__":
    nltk.download('punkt')
    main()
