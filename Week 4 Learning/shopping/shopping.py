import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
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
    Load purchase data from a CSV file `filename` and convert it into a list of
    lists of evidence and a list of labels. Returns a tuple (evidence, labels).

    Evidence should be a list of lists, where each list contains the following
    values in order:
        - Administrative, in full
        - Administrative_Duration, a floating-point number
        - Informational, in full
        - Informational_Duration, a floating-point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating-point number
        - BounceRates, a floating-point number
        - ExitRates, a floating-point number
        - PageValues, a floating-point number
        - SpecialDay, a floating-point number
        - Month, an index from 1 (January) to 12 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 1 (Returning_Visitor), 2 (New_Visitor), or 3 (Other)
        - Weekend, an integer 0 (if false) or 1 (if true)

    Labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true and 0 otherwise.
    """

    # Initialize lists to store evidence and labels
    evidence = []
    labels = []

    # Mapeando nomes de meses para números
    month_mapping = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }

    # Mapeamento para VisitorType
    visitor_mapping = {'Returning_Visitor': 1, 'New_Visitor': 2, 'Other': 3}

    # Abra o arquivo CSV e leia os dados
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pule o cabeçalho

        for row in reader:
            # Verifique se a lista row tem exatamente 18 elementos
            if len(row) == 18:
                # Mapeie VisitorType para valores numéricos
                visitor_type = visitor_mapping.get(row[15], 0)

                # Mapeie o campo Weekend para 0 ou 1
                weekend = 1 if row[17].lower() == 'TRUE' else 0

                # Transforme o mês em um número usando month_mapping
                month_number = month_mapping.get(row[10], 0)  # Usando month_number aqui


                # Extrair evidência da linha atual
                current_evidence = [
                    float(row[0]), float(row[1]), float(row[2]), float(row[3]),
                    int(row[4]), float(row[5]), float(row[6]), float(row[7]),
                    float(row[8]), float(row[9]), month_number,
                    int(row[11]), int(row[12]), int(row[13]), int(row[14]),
                    visitor_type, weekend
                ]

                # Adicionar evidência à lista de evidências
                evidence.append(current_evidence)

                # Adicionar rótulo à lista de rótulos
                labels.append(1 if row[16] == 'TRUE' else 0)

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
        if true_label == 1 and pred_label == 1:
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
    specificity = true_negatives / (true_negatives + false_positives)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
