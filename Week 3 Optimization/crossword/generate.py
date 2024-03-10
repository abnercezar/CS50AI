import sys

from crossword import Crossword, Variable
# from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Crie uma nova geração de palavras cruzadas CSP.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Retorna uma matriz 2D que representa uma determinada atribuição.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Imprima a atribuição de palavras cruzadas no terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Salve a tarefa de palavras cruzadas em um arquivo de imagem.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Imponha a consistência do nó e do arco e, em seguida, resolva o CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Atualize `self.domains` de forma que cada variável seja consistente com o nó.
        (Remova quaisquer valores que sejam inconsistentes com o unário de uma variável
         restrições; neste caso, o comprimento da palavra.)
        """
        # Para cada variável, filtra os valores e o comprimento
        for variable in self.domains:
            self.domains[variable] = {value for value in self.domains[variable]
                                      if len(value) == variable.length}

    def revise(self, x, y):
        """
        Torne a variável `x` consistente com a variável `y`.
        Para fazer isso, remova valores de `self.domains[x]` para os quais não há
        possível valor correspondente para `y` em `self.domains[y]`.

        Retorna True se foi feita uma revisão no domínio de `x`; retornar
        Falso se nenhuma revisão foi feita.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return revised

        i, j = overlap

        # Cria um conjunto de valores em `self.domains[x]` que tenham um valor correspondente
        # valor em `self.domains[y]`
        consistent_values = {
            x_value for x_value in self.domains[x]
            if any(y_value for y_value in self.domains[y]
                   if x_value[i] == y_value[j] and x_value != y_value)
        }

        # Cria um conjunto de valores inconsistentes em `self.domains[x]`
        inconsistent_values = self.domains[x] - consistent_values

        # Se o conjunto de valores consistentes for um subconjunto adequado de `self.domains[x]`,
        # atualize `self.domains[x]` e retorne True
        if inconsistent_values:
            self.domains[x] = consistent_values
            revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Atualize `self.domains` de forma que cada variável seja consistente em arco.
        Se `arcs` for Nenhum, comece com a lista inicial de todos os arcos do problema.
        Caso contrário, use `arcs` como a lista inicial de arcos para torná-los consistentes.

        Retorna True se a consistência do arco for aplicada e nenhum domínio estiver vazio;
        retorne False se um ou mais domínios ficarem vazios.
        """
        # Inicializa a pilha com todos os arcos se 'arcs' for None
        if arcs is None:
            # Se 'arcs' for None, cria uma lista de todos os arcos possíveis
            arcs = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]

        # Inicializa uma fila (deque) com os arcos
        queue = deque(arcs)
        # Flag para verificar se ocorreu alguma revisão durante o processo
        removed = False

        # Loop principal para processar os arcos na fila
        while queue:
            # Remove um arco da fila
            x, y = queue.popleft()
            # Chama a função 'revise' para tornar 'x' arc consistente com 'y'
            if self.revise(x, y):
                # Se o domínio de 'x' ficar vazio após a revisão, retorna False
                if not self.domains[x]:
                    return False
                # Adiciona os arcos envolvendo os vizinhos de 'x' à fila (exceto o arco atual 'x, y')
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
                # Marca que houve uma revisão
                removed = True
        # Retorna True e um dicionário vazio, indicando que a consistência foi mantida
        return True, {}

    def assignment_complete(self, assignment):
        """
        Retorna True se a `atribuição` for concluída (ou seja, atribui um valor a cada
        variável de palavras cruzadas); retorne False caso contrário.
        """
        # A tarefa será concluída se cada variável receber um valor no dicionário
        # de atribuição, e armazena apenas um valor, e teste os conflitos aqui
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Retorna True se `atribuição` for consistente (ou seja, as palavras cabem nas palavras cruzadas
        quebra-cabeça sem personagens conflitantes); retorne False caso contrário.
        """
        # Verifica se todas as variáveis estão presentes na atribuição
        # for variable in self.crossword.variables:
        #   if variable not in assignment:
        #       return False

        # Verifica se cada valor atribuído é distinto
        distinct = set()
        if len(assignment) != len(set(assignment)):
            # Se o número de valores únicos no dicionário de atribuição for diferente do número total de atribuições,
            # então há valores repetidos, o que é inconsistente
            return False

        # Verifica a consistência do nó
        for variable, value in assignment.items():
            # Verifica se o comprimento do valor atribuído à variável é igual ao comprimento da própria variável
            if len(value) != variable.length:
                # Se o comprimento não corresponder, a atribuição é inconsistente
                return False
            # Adiciona o valor à lista de valores distintos para posterior verificação de conflitos
            distinct.add(value)

        # Verifica a consistência do arco
        for variable1, value1 in assignment.items():
            for variable2, value2 in assignment.items():
                # Evita comparar uma variável consigo mesma
                if variable1 == variable2:
                    continue
                # Obtém as posições de sobreposição entre as duas variáveis
                overlaps = self.crossword.overlaps.get((variable1, variable2))
                if overlaps is not None:
                    i, j = overlaps
                    # Verifica se os caracteres nas posições de sobreposição são iguais
                    if value1[i] != value2[j]:
                        # Se os caracteres não forem iguais, há um conflito e a atribuição é inconsistente
                        return False

        # Se todas as verificações passaram sem retornar False, então a atribuição é consistente
        return True

    def order_domain_values(self, var, assignment):
        """
        Retorna uma lista de valores no domínio de `var`, em ordem por
        o número de valores que eles excluem para variáveis ​​vizinhas.
        O primeiro valor da lista, por exemplo, deve ser aquele
        que exclui o menor número de valores entre os vizinhos de `var`.
        """
        # Encontre todos os vizinhos da variável fornecida
        neighbors = self.crossword.neighbors(var)

        # Faça a tarefa e veja se alguns vizinhos já têm uma palavra atribuída
        for variable in assignment:
            # Se a variável estiver em vizinhos e em atribuição, ela já possui valor e não é considerada vizinha
            if variable in neighbors:
                neighbors.remove(variable)

        # Inicializa uma lista de resultados que serão ordenados de acordo com a heurística (valores menos restritivos)
        result = []

        for value in self.domains[var]:
            ruled_out = 0  # Acompanhe a quantidade de opções no domínio que serão excluídas para variáveis ​​vizinhas
            # Classifique os vizinhos pelo número de opções em seu domínio que serão excluídas
            sorted_neighbors = sorted(neighbors, key=lambda x: sum(
                overlap for overlap in self.crossword.overlaps[x, var]), reverse=True)

            for neighbor in sorted_neighbors:
                # Se houver uma sobreposição entre as variáveis,
                # Então um deles não poderá mais ter esse valor de domínio
                for variable in self.domains[neighbor]:
                    overlap = self.crossword.overlaps[var, neighbor]

                    # Se houver uma sobreposição e os caracteres sobrepostos não forem iguais,
                    # Então o vizinho não pode ter este valor de domínio
                    if overlap:
                        a, b = overlap
                        if value[a] != variable[b]:
                            ruled_out += 1
            # Armazena o valor com a quantidade de opções do domínio que serão excluídas para variáveis ​​vizinhas
            result.append([value, ruled_out])

        # Classifica todos os valores pelo número de opções no domínio que serão excluídas para variáveis ​​vizinhas
        result = sorted(result, key=lambda x: x[1])

        return [i[0] for i in result]  # Retorna apenas a lista de valores, sem o parâmetro Ruled_out

    def select_unassigned_variable(self, assignment):
        """
        Retorna uma variável não atribuída que ainda não faz parte da `atribuição`.
        Escolha a variável com o número mínimo de valores restantes
        em seu domínio. Em caso de empate, escolha a variável com maior
        grau. Se houver empate, qualquer uma das variáveis ​​empatadas é aceitável
        valores de retorno.
        """
        unassigned = set(var for var in self.crossword.variables if var not in assignment)

        # Priorize variáveis ​​com menos valores restantes em seu domínio
        order = sorted(unassigned, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

        return order[0]

    def backtrack(self, assignment):
        """
        Usando a pesquisa de retrocesso, tome como entrada uma atribuição parcial para o
        palavras cruzadas e retorne uma tarefa completa, se possível.
        `atribuição` é um mapeamento de variáveis ​​(chaves) para palavras (valores).
        Se nenhuma atribuição for possível, retorne None.
        """
        # Verifica se a atribuição está completa
        if self.assignment_complete(assignment):
            # Se estiver completa, retorna a atribuição

            return assignment

        # Seleciona uma variável não atribuída para atribuir um valor
        var = self.select_unassigned_variable(assignment)

        # Itera sobre os valores do domínio da variável selecionada, ordenados por algum critério
        for value in self.order_domain_values(var, assignment):

            # Atribui o valor à variável na atribuição
            assignment[var] = value

            # Verifica se a atribuição atual é consistente
            if self.consistent(assignment):

                # Aplica AC3 para realizar inferências
                success, inferences = self.ac3(arcs=[(y, var) for y in self.crossword.neighbors(var)])

                # Se AC3 foi bem-sucedido
                if success:

                    # Atualiza a atribuição com as inferências
                    assignment.update(inferences)

                    # Chama recursivamente a função backtrack para continuar a busca
                    result = self.backtrack(assignment)

                    # Se a busca retornar uma atribuição completa, a retorna
                    if result is not None:

                        return result

                # Desfaz a atribuição atual antes de tentar o próximo valor
                assignment.pop(var)

        # Se nenhum valor do domínio leva a uma solução completa, retorna None

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
