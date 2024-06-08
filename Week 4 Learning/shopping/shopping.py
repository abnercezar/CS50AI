import csv
import sys
import numpy as np
print(sys.argv)  # Isso imprimirá a lista de argumentos passados ao script


from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python shopping.py <filename>")
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet
    evidence, labels = load_data(sys.argv[1])

    # Determine sizes for train and test sets
    total_samples = len(evidence)
    test_size = 0.1  # 10% for testing, adjust as needed
    train_size = 0.9

    print(f"Total samples: {total_samples}")
    print(f"Test size: {test_size}, Train size: {train_size}")

    # Check if total samples are sufficient for splitting
    if total_samples == 0 or (total_samples * train_size) < 1:
        print("Número de amostras insuficiente para divisão.")
        return

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=test_size, train_size=train_size, random_state=42
    )

    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

    # Convert evidence and labels to NumPy arrays
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

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
            # Verifique se a lista row tem pelo menos 19 elementos
            if len(row) >= 19:
                # Mapeie VisitorType para valores numéricos
                visitor_type = visitor_mapping.get(row[8], 0)

                # Mapeie o campo Weekend para 0 ou 1
                weekend = 1 if row[18] == 'TRUE' else 0

                # Extrair evidência da linha atual
                current_evidence = [
                    float(row[0]), float(row[1]), float(row[2]), float(row[3]),
                    int(row[4]), float(row[5]), float(row[6]), float(row[7]),
                    float(row[9]), month_mapping[row[10]], int(row[11]),
                    int(row[12]), int(row[13]), int(row[14]), visitor_type, weekend
                ]

                # Adicionar evidência à lista de evidências
                evidence.append(current_evidence)

                # Adicionar rótulo à lista de rótulos
                labels.append(1 if row[17] == 'TRUE' else 0)
            else:
                print(f"A linha {row} não possui dados suficientes.")

    return evidence, labels


def train_model(evidence, labels):
    """
    Dada uma lista de listas de evidências e uma lista de rótulos, retorne um
    modelo ajustado de k-vizinho mais próximo (k = 1) treinado nos dados.
    """
    # Inicialize o classificador KNeighborsClassifier com k=1
    model = KNeighborsClassifier(n_neighbors=1)

    # Imprima os tipos de dados das variáveis evidence e labels
    print(f"Tipo de dados de evidence: {type(evidence)}")
    print(f"Tipo de dados de labels: {type(labels)}")

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
