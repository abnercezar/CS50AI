import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Analise um diretório de páginas HTML e verifique links para outras páginas.
    Retorne um dicionário onde cada chave é uma página e os valores são
    uma lista de todas as outras páginas do corpus vinculadas pela página.
    """
    pages = dict()

    # Extraia todos os links de arquivos HTML
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Incluir apenas links para outras páginas no corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Retornar uma distribuição de probabilidade sobre qual página visitar em seguida,
    dada uma página atual.

    Com probabilidade `damping_factor`, escolha um link aleatoriamente
    vinculado por `página`. Com probabilidade `1 - fator de amortecimento`, escolha
    um link escolhido aleatoriamente em todas as páginas do corpus.
    """
    # Inicializa um dicionário vazio para armazenar as probabilidades de transição
    transition_probability = {}

    # Conta o número total de páginas do corpus
    num_pages = len(corpus)

    # Conta o número total de links em uma página específica do corpus
    num_links = len(corpus[page]) if page in corpus else num_pages

    # Itera em cada página do corpus.
    for p in corpus:
        # Define a probabilidade de transição inicial para cada página como a mesma, que é
        # (1 - fator de amortecimento) dividido pelo número total de páginas. Isso representa a
        # probabilidade de um surfista aleatório pular para qualquer página do corpus.
        transition_probability[p] = (1 - damping_factor) / num_pages

    # Itera em cada página vinculada à página atual
    for linked_page in corpus.get(page, []):
        # Adiciona ao valor da probabilidade de transição da página vinculada o fator de amortecimento
        # dividido pelo número total de links na página atual. Isso representa a probabilidade de um surfista
        # permanecer na página atual e ir para a página vinculada.
        transition_probability[linked_page] += damping_factor / num_links

    # Retorna o dicionário com as probabilidades de transição
    return transition_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Retorne valores de PageRank para cada página amostrando `n` páginas
    de acordo com o modelo de transição, começando com uma página aleatória.

    Retorne um dicionário onde as chaves são nomes de páginas e os valores são
    seu valor estimado de PageRank (um valor entre 0 e 1). Todos
    Os valores do PageRank devem somar 1.
    """
    # Calcula o número total de páginas no corpus
    num_pages = len(corpus)

    # Cria um dicionário onde cada página do corpus é uma chave e a classificação inicial é definida como 0
    ranks = {page: 0 for page in corpus}

    # Seleciona uma página aleatória do corpus para iniciar o algoritmo PageRank
    current_page = random.choice(list(corpus.keys()))

    # Executa o algoritmo PageRank 'n' vezes
    for _ in range(n):
        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            list(probabilities.keys()), weights=list(probabilities.values()), k=1
        )[0]

        # Atualiza a classificação da página atual
        ranks[current_page] += 1 / n

    # Retorna o dicionário com as classificações das páginas
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Retorne valores de PageRank para cada página atualizando iterativamente
    Valores do PageRank até a convergência.

    Retorne um dicionário onde as chaves são nomes de páginas e os valores são
    seu valor estimado de PageRank (um valor entre 0 e 1). Todos
    Os valores do PageRank devem somar 1.
    """
    # Inicializa o dicionário de classificações com uma classificação igual para todas as páginas
    ranks = {page: 1 / len(corpus) for page in corpus}

    # Loop infinito que só termina quando as classificações não mudam significativamente entre duas iterações
    while True:
        # Inicializa um novo dicionário para armazenar as novas classificações
        new_ranks = {}

        # Itera em cada página do corpus
        for page in corpus:
            # Define a classificação inicial para a página atual
            rank = (1 - damping_factor) / len(corpus)

            # Itera em cada página vinculada à página atual
            for linked_page in corpus:
                
                # Verifica se uma página não possui links
                if len(corpus[linked_page]) == 0:
                    rank += damping_factor * ranks[linked_page] / len(corpus)

                # Se a página atual está vinculada à página vinculada, adiciona ao valor da classificação da página atual
                # o produto do fator de amortecimento e da classificação da página vinculada, dividido pelo número total de páginas vinculadas
                if page in corpus[linked_page]:
                    rank += (
                        damping_factor * ranks[linked_page] / len(corpus[linked_page])
                    )

            # Armazena a nova classificação da página atual
            new_ranks[page] = rank

        # Normaliza os valores para garantir que a soma seja 1
        total_rank = sum(new_ranks.values())
        new_ranks = {page: rank / total_rank for page, rank in new_ranks.items()}

        # Verifica se as classificações não mudaram significativamente entre duas iterações
        if all(abs(new_ranks[page] - ranks[page]) < 0.000001 for page in corpus):
            # Se não houve mudança significativa, interrompe o loop
            break

        # Atualiza as classificações com as novas classificações
        ranks = new_ranks
    # Retorna o dicionário final com as classificações
    return ranks


if __name__ == "__main__":
    main()
