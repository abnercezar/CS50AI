import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
   Carregue os dados da imagem do diretório `data_dir`.

    Suponha que `data_dir` tenha um diretório nomeado após cada categoria, numerado
    0 a NUM_CATEGORIES - 1. Dentro de cada diretório de categoria haverá alguns
    número de arquivos de imagem.

    Retorna a tupla `(imagens, rótulos)`. `images` deve ser uma lista de todas
    das imagens no diretório de dados, onde cada imagem é formatada como um
    numpy ndarray com dimensões IMG_WIDTH x IMG_HEIGHT x 3. `labels` devem
    ser uma lista de rótulos inteiros, representando as categorias de cada um dos
    `imagens` correspondentes.
    """
    # Inicializa listas vazias para armazenar imagens e rótulos
    images = []
    labels = []

    # Itera por cada categoria (de 0 a NUM_CATEGORIES - 1)
    for category in range(NUM_CATEGORIES):
        # Constrói o caminho do diretório para a categoria atual
        category_directory = os.path.join(data_dir, str(category))

        # Verifica se o diretório da categoria existe
        if os.path.isdir(category_directory):
            # Itera por cada arquivo no diretório da categoria atual
            for filename in os.listdir(category_directory):
                # Constrói o caminho completo para o arquivo de imagem
                image_path = os.path.join(category_directory, filename)

                # Lê a imagem usando o OpenCV
                image = cv2.imread(image_path)

                # Redimensiona a imagem para IMG_WIDTH x IMG_HEIGHT
                image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

                # Adiciona a imagem redimensionada à lista de imagens
                images.append(image)

                # Adiciona a categoria (rótulo) à lista de rótulos
                labels.append(category)

    # Retorna as listas de imagens e rótulos como uma tupla
    return images, labels


def get_model():
    """
   Retorna um modelo de rede neural convolucional compilado. Suponha que o
    `input_shape` da primeira camada é `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    A camada de saída deve ter unidades `NUM_CATEGORIES`, uma para cada categoria.
    """
    # Cria uma rede neural convolucional
    model = tf.keras.models.Sequential([

        # Camada convolucional. Aprende 32 filtros usando um kernel 3x3
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Camada de max-pooling, usando um tamanho de pool 2x2
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Unidades flatten
        tf.keras.layers.Flatten(),

        # Adiciona uma camada oculta com dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Adiciona uma camada de saída
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Treina a rede neural
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
