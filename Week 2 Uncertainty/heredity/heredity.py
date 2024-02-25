import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():  # A função primeiro carrega dados de um arquivo em um dicionário people

    # Verifique o uso adequado
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Acompanhe as probabilidades genéticas e características de cada pessoa
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Calcule e retorne uma probabilidade conjunta.

    A probabilidade retornada deve ser a probabilidade de que
        * todos no conjunto `one_gene` possuem uma cópia do gene, e
        * todos no conjunto `two_genes` possuem duas cópias do gene, e
        * todos que não estão em `one_gene` ou `two_gene` não possuem o gene, e
        * todos no conjunto `have_trait` possuem a característica, e
        * todos que não estão no set` have_trait` não possuem a característica.
    """

    joint_prob = 1

    # Itere todas as pessoas da família:
    for person in people:

        person_trait_value = 1
        person_gene_count = (2 if person in two_genes else 1 if person in one_gene else 0)
        has_trait = person in have_trait
        mother = people[person]['mother']
        father = people[person]['father']

        # Se a pessoa não tiver pais, use a probabilidade genética padrão:
        if not mother and not father:
            person_trait_value *= PROBS['gene'][person_gene_count]

        # Caso contrário, será necessário calcular a probabilidade de num_genes dos pais:
        else:
            mother_prob = inherit_prob(mother, one_gene, two_genes)
            father_prob = inherit_prob(father, one_gene, two_genes)

            if person_gene_count == 2:
                person_trait_value *= mother_prob * father_prob
            elif person_gene_count == 1:
                person_trait_value *= (1 - mother_prob) * father_prob + (1 - father_prob) * mother_prob
            else:
                person_trait_value *= (1 - mother_prob) * (1 - father_prob)

        # Multiplique pela probabilidade da pessoa com genes X ter/não ter o traço:
        person_trait_value *= PROBS['trait'][person_gene_count][has_trait]

        joint_prob *= person_trait_value

    # Retorna a probabilidade conjunta calculada deste 'mundo possível'
    return joint_prob


def inherit_prob(parent_name, one_gene, two_genes):
    """
    função auxiliar joint_probability

    Retorna a probabilidade de um pai dar uma cópia do gene mutado ao filho.

    Leva:
    - parent_name - o nome do pai
    - one_gene - conjunto de pessoas que possuem 1 cópia do gene
    - two_genes - conjunto de pessoas que possuem duas cópias do gene.
    """

    if parent_name in two_genes:
        return 1 - PROBS['mutation']
    elif parent_name in one_gene:
        return 0.5
    else:
        return PROBS['mutation']


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Adicione às `probabilidades` uma nova probabilidade conjunta `p`.
    Cada pessoa deve ter suas distribuições de “genes” e “características” atualizadas.
    Qual valor para cada distribuição é atualizado depende se
    a pessoa está em `have_gene` e `have_trait`, respectivamente.
    """

    for person in probabilities:
        if p is not None:
            if person in one_gene:
                probabilities[person]['gene'][1] += p
            elif person in two_genes:
                probabilities[person]['gene'][2] += p
            else:
                probabilities[person]['gene'][0] += p

            if person in have_trait:
                probabilities[person]['trait'][True] += p
            else:
                probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Atualize as `probabilidades` de modo que cada distribuição de probabilidade
    é normalizado (ou seja, soma 1, com proporções relativas iguais).
    """
    for person in probabilities:
        total = sum(probabilities[person]['gene'].values())
        if total != 0:
            for gene, probability in probabilities[person]['gene'].items():
                probabilities[person]['gene'][gene] = probability / total

        total = sum(probabilities[person]['trait'].values())
        if total != 0:
            for trait, probability in probabilities[person]['trait'].items():
                probabilities[person]['trait'][trait] = probability / total


if __name__ == "__main__":
    main()
