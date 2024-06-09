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
    Carregue os dados de compra de um arquivo CSV `filename` e converta-os em uma lista de
    listas de evidências e uma lista de rótulos. Retorna uma tupla (evidências, rótulos).

    A evidência deve ser uma lista de listas, onde cada lista contém o seguinte
    valores em ordem:
        - Administrativo, na íntegra
        - Administrative_Duration, um número de ponto flutuante
        - Informativo, na íntegra
        - Informational_Duration, um número de ponto flutuante
        - ProductRelated, um número inteiro
        - ProductRelated_Duration, um número de ponto flutuante
        - BounceRates, um número de ponto flutuante
        - ExitRates, um número de ponto flutuante
        - PageValues, um número de ponto flutuante
        - SpecialDay, um número de ponto flutuante
        - Mês, um índice de 1 (janeiro) a 12 (dezembro)
        - Sistemas Operacionais, um número inteiro
        - Navegador, um número inteiro
        - Região, um número inteiro
        - TrafficType, um número inteiro
        - VisitorType, um número inteiro 1 (Returning_Visitor), 2 (New_Visitor) ou 3 (Outro)
        - Fim de semana, um número inteiro 0 (se for falso) ou 1 (se for verdadeiro)

    Os rótulos devem ser a lista correspondente de rótulos, onde cada rótulo
    é 1 se Receita for verdadeira e 0 caso contrário.
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
    visitor_mapping = {'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 2}

    # Abra o arquivo CSV e leia os dados
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pule o cabeçalho

        for row in reader:
            if len(row) == 18:  # Verifica se a lista row tem exatamente 18 elementos
                # Mapeie VisitorType para valores numéricos
                visitor_type = visitor_mapping.get(row[15], 0)

                # Mapeie o campo Weekend para 0 ou 1
                weekend = 1 if row[16].strip().lower() == 'true' else 0

                # Transforme o mês em um número usando month_mapping
                month_number = month_mapping.get(row[10], 0)

                # Extrair evidência da linha atual
                current_evidence = [
                    int(row[0]), float(row[1]), int(row[2]), float(row[3]),
                    int(row[4]), float(row[5]), float(row[6]), float(row[7]),
                    float(row[8]), float(row[9]), month_number,
                    int(row[11]), int(row[12]), int(row[13]), int(row[14]),
                    visitor_type, weekend
                ]

                # Adicionar evidência à lista de evidências
                evidence.append(current_evidence)

                # Adicionar rótulo à lista de rótulos
                labels.append(1 if row[17].strip().lower() == 'true' else 0)

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
