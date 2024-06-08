import csv
import sys
print(sys.argv)  # Isso imprimirá a lista de argumentos passados ao script


from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python shopping.py <filename>")
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Carregue dados de compras de um arquivo CSV `filename` e converta em uma lista de
    listas de evidências e uma lista de rótulos. Retorna uma tupla (evidências, rótulos).

    evidência deve ser uma lista de listas, onde cada lista contém o
    seguintes valores, em ordem:
        - Administrativo, na sua totalidade
        - Administrative_Duration, um número de ponto flutuante
        - Informativo, na íntegra
        - Informational_Duration, um número de ponto flutuante
        - ProductRelated, um número inteiro
        - ProductRelated_Duration, um número de ponto flutuante
        - BounceRates, um número de ponto flutuante
        - ExitRates, um número de ponto flutuante
        - PageValues, um número de ponto flutuante
        - SpecialDay, um número de ponto flutuante
        - Mês, um índice de 0 (janeiro) a 11 (dezembro)
        - Sistemas Operacionais, um número inteiro
        - Navegador, um todo
        - Região, um número inteiro
        - TrafficType, um número inteiro
        - VisitorType, um número inteiro 0 (não retornando) ou 1 (retornando)
        - Fim de semana, um número inteiro 0 (se for falso) ou 1 (se for verdadeiro)

        rótulos devem ser a lista correspondente de rótulos, onde cada rótulo
        é 1 se Receita for verdadeira e 0 caso contrário.
        """


    # Inicialize as listas para armazenar evidências e rótulos
    evidence = []
    labels = []

    # Mapeamento de mês para número
    month_mapping = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    # Mapeamento para VisitorType
    visitor_mapping = {'Returning_Visitor': 1, 'New_Visitor': 2, 'Other': 3}

    # Abra o arquivo CSV e leia os dados
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # Pule o cabeçalho

        for row in reader:
            print("Row:", row)
        # Extrair evidência da linha atual
            current_evidence = [
                float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x for x in [
                    row[0], row[2], row[4], row[6],
                    visitor_mapping.get(row[8], 0),  # Usando o mapeamento para VisitorType
                    1 if row[9] == 'TRUE' else 0,
                    month_mapping[row[10]],
                    *[float(y) if isinstance(y, str) and y.replace('.', '', 1).isdigit() else 0.0 for y in row[11:16] if y != ''] + [0.0] * (6 - len(row[11:16])),
                ]
            ]
            print("Current Evidence:", current_evidence)

            # Adicionar evidência à lista de evidências
            evidence.append(current_evidence)

            # Adicionar rótulo à lista de rótulos
            labels.append(1 if row[17] == 'TRUE' else 0)

    return evidence, labels


def train_model(evidence, labels):
    """
    Dada uma lista de listas de evidências e uma lista de rótulos, retorne um
    modelo ajustado de k-vizinho mais próximo (k = 1) treinado nos dados.
    """
    # Inicialize o classificador KNeighborsClassifier com k=1
    model = KNeighborsClassifier(n_neighbors=1)

    # Treine o modelo com os dados de evidência e rótulos fornecidos
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Dada uma lista de rótulos reais e uma lista de rótulos previstos,
    retornar uma tupla (sensibilidade, especificidade).

    Suponha que cada rótulo seja 1 (positivo) ou 0 (negativo).

    `sensibilidade` deve ser um valor de ponto flutuante de 0 a 1
    representando a "taxa positiva verdadeira": a proporção de
    rótulos positivos reais que foram identificados com precisão.

    `especificidade` deve ser um valor de ponto flutuante de 0 a 1
    representando a "taxa verdadeiramente negativa": a proporção de
    rótulos negativos reais que foram identificados com precisão.
    """
    # Inicialize contadores para verdadeiros positivos, verdadeiros negativos, falsos positivos, e falsos negativos
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    # Calcule os valores dos contadores
    for true_label, pred_label in zip(labels, predictions):
        if true_label == 1 and pred_label ==1:
            true_positives += 1
        elif true_label == 0 and pred_label == 0:
            true_negatives += 1
        elif true_label == 0 and pred_label == 1:
            false_positives += 1
        elif true_label == 1 and pred_label == 0:
            false_negatives += 1

    # Calcule a sensibilidade (taxa de verdadeiros positivos)
    sensitivity = true_positives / (true_positives + false_negatives)

    # Calcule a especifidade (taxa de verdadeiros negativos)
    specificity = true_negatives / (true_negative + false_positives)

    return sensitivity, specificity

if __name__ == "__main__":
    main()
