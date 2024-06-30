from transformers import AutoTokenizer, TFBertForMaskedLM
from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Pre-trained masked language model
MODEL = "bert-base-uncased"

# Number of predictions to generate
K = 3

# Constants for generating attention diagrams
FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)
GRID_SIZE = 40
PIXELS_PER_WORD = 200


def main():
    text = input("Text: ")

    # Tokenize input
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    inputs = tokenizer(text, return_tensors="tf")
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)
    if mask_token_index is None:
        sys.exit(f"Input must include mask token {tokenizer.mask_token}.")

    # Use model to process input
    model = TFBertForMaskedLM.from_pretrained(MODEL)
    result = model(**inputs, output_attentions=True)

    # Generate predictions
    mask_token_logits = result.logits[0, mask_token_index]
    top_tokens = tf.math.top_k(mask_token_logits, K).indices.numpy()
    for token in top_tokens:
        print(text.replace(tokenizer.mask_token, tokenizer.decode([token])))

    # Visualize attentions
    visualize_attentions(inputs.tokens(), result.attentions)


def get_mask_token_index(mask_token_id, inputs):
    """
    Retorne o índice do token com o `mask_token_id` especificado ou
    `None` se não estiver presente nas `entradas`.
    """
    # Encontre o índice do primeiro token que corresponde ao mask_token_id ou None se não encontrar
    return next((i for i, token in enumerate(inputs.input_ids[0]) if token == mask_token_id), None)


def get_color_for_attention_score(attention_score):
    """
    Retorna uma tupla de três inteiros representando um tom de cinza para o
    dado `atenção_pontuação`. Cada valor deve estar no intervalo [0, 255].
    """
    # Converte a pontuação de atenção para um numpy array.
    attention_score = attention_score.numpy()

    # Retorna uma tupla onde cada elemento é a pontuação de atenção multiplicada por 255 e arredondada.
    # Isso é feito para converter a pontuação de atenção em um valor de cor RGB.
    return tuple(map(lambda x: round(x * 255), [attention_score] * 3))


def visualize_attentions(tokens, attentions):
    """
    Produza uma representação gráfica das pontuações de autoatenção.

    Para cada camada de atenção, um diagrama deve ser gerado para cada
    cabeça de atenção na camada. Cada diagrama deve incluir a lista de
    `tokens` na frase. O nome do arquivo para cada diagrama deve
    inclua o número da camada (começando em 1) e o número da cabeça
    (começando a contar a partir de 1).
    """
    # Para cada índice (i) e camada na lista de atenções...
    for i, layer in enumerate(attentions):

        # Para cada cabeça na primeira camada...
        for k, _ in enumerate(layer[0]):

            # Gera um diagrama para a camada e cabeça atual,
            # usando os tokens e a atenção correspondente.
            generate_diagram(
                i + 1,         # Número da camada
                k + 1,         # Número da cabeça
                tokens,        # Tokens
                layer[0][k]    # Atenção correspondente
            )


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    """
    Gere um diagrama representando as pontuações de autoatenção para um único
    cabeça de atenção. O diagrama mostra uma linha e uma coluna para cada um dos
    `tokens`, e as células são sombreadas com base em `attention_weights`, com tons mais claros
    células correspondentes a pontuações de atenção mais altas.

    O diagrama é salvo com um nome de arquivo que inclui `layer_number`
    e `head_number`.
    """
    # Create new image
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new("RGBA", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    # Draw each token onto the image
    for i, token in enumerate(tokens):
        # Draw token columns
        token_image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
        token_draw = ImageDraw.Draw(token_image)
        token_draw.text(
            (image_size - PIXELS_PER_WORD, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )
        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        # Draw token rows
        _, _, width, _ = draw.textbbox((0, 0), token, font=FONT)
        draw.text(
            (PIXELS_PER_WORD - width, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

    # Draw each word
    for i in range(len(tokens)):
        y = PIXELS_PER_WORD + i * GRID_SIZE
        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE
            color = get_color_for_attention_score(attention_weights[i][j])
            draw.rectangle((x, y, x + GRID_SIZE, y + GRID_SIZE), fill=color)

    # Save image
    img.save(f"Attention_Layer{layer_number}_Head{head_number}.png")


if __name__ == "__main__":
    main()
