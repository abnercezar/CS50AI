import sys
from itertools import chain, product

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        self.arcs = [] # Inicianiza 'self.arcs'
        self.neighbors = {} # Inicializa 'self.neighbors'


    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
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
        Print crossword assignment to the terminal.
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
        Save crossword assignment to an image file.
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
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            # Crie um novo conjunto para armazenar palavras para remover
            words_to_remove = set()

            # Verifica cada palavra no domínio da variável
            for word in self.domains[variable]:

                # Se o comprimento da palavra não for igual ao comprimento de variável
                # adicione a palavra ao conjunto de palavras  aserem removidas
                if len(word) != variable.length:
                    words_to_remove.add(word)

            # Remoeve todas as palavras do conjunto do domínio da variável
            self.domains[variable] -= words_to_remove


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        values_to_remove = set()

        # Iterar sobre cda valor em self.domains[x]
        for value in self.domains[x]:

            # Verifica se existe algum valor em self.domains[y] que satisfaça a restrição binária com valor
            if not any(value == y_value for y_value in self.domains[y]):

                # Caso contrário, adicione valor ao conjunto de valores a serem removidos
                values_to_remove.add(value)

        # Remova os valores de self.domains[x]
        self.domains[x] -= values_to_remove

        # Retorna True se algum valor foi removido, False caso contrário
        return bool(values_to_remove)


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Se arcs for None, inicialize-o com todos os arcos possíveis no problema
        if arcs is None:
            arcs = self.arcs

        for arc in arcs:
            variable1, variable2 = arc

        # Crie uma lista de trabalho a partir dos arcos iniciais.
        work_list = list(arcs)
        y = None

        # Embora existam arcos na lista de trabalho, destaque o primeiro arco e torne-o consistente
        while work_list:
            arc = work_list.pop(0)
            print(arc)
            arc = (variable1, variable2)
            x, y = arc[0], arc[1]
            if y is None or x != y:
                for neighbor in self.neighbors[x]:
                    work_list.append((neighbor, x))
                if self.revise(x, y):

                        # Se o domínio de x ficar vazio, retorne False
                        if not self.domains[x]:
                            return False

                        # Para cada vizinho z de x diferente de y, adicione o arco (z, x) à lista de trabalho.
                        for z in self.neighbors[x]:
                            if z != y:
                                work_list.append((z, x))

            # Se todos os domínios não estiverem vazios, retorne True.
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Itere sobre cada variável nas palavras cruzadas
        for variable in self.crossword.variables:

            # Se a variável não receber um valor na atribuição, retorne False
            if variable not in assignment:
                return False

        # Se todas as varíaveis receberem um valor na atribuição, retorne True
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Iterar sobre cada um na tarefa
        for variable in assignment:
            # Obtém o valor atribuído á variável
            value = assignment[variable]

            # Itera sobre cada vizinho da variável
            for neighbor in variable.neighbors:
                # Se o vizinho não estiver na tarefa, pule-a
                if neighbor not in assignment:
                    continue

                # Obtém o valor atribuído ao vizinho
                neighbor_value = assignment[neighbor]

                # Verifica se os valores atribuídos à variável e ao seu vizinho são iguais
                if value == neighbor_value:
                    # Se forem iguais, a atribuição é inconsistente
                    return False

                # Verifica se os comprimentos dos valores atribuídos á variável e ao seu vizinho são diferentes
                if len(value) != len(neighbor_value):
                    # Se os comprimentos forem diferentes, a atribuição é inconsistente
                    return False

        # Se a função não retornou False, a atribuição é consistente
                return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Crie um dicionário para armazenar o número de valores descartados por cada valor de domínio
        values_to_count = {}

        # Itera sobre cada valor no domínio de 'var'
        for value in var.domain:

            # Inicializa a contagem de valores descartados para 0
            count = 0

            # Itera sobre cada vizinho de 'var'
            for neighbor in var.neighbors:
                # Se o vizinho não estiver na atribuição, ainda não foi atribuído um valor
                if neighbor not in assignment:
                    # Itera sobre cada valor no domínio do vizinho
                    for neighbor_value in self.crossword.domains[neighbor]:
                        # Se o vizinho puder assumir o valor atual e o valor atual não for o valor de 'var'
                        if self.crossword.overlaps[(var.index, neighbor.index)] == value or self.crossword.overlaps[(neighbor.index, var.index)] == neighbor_value:
                            # Se o vizinho não puder assumir o valor atual, aumente a contagem
                            count += 1

            # Armazena a contagem no dicionário
            values_to_count[value] = count

        # Classifica as chaves do dicionário pela contagem correspondente em ordem crescente
        sorted_values = sorted(values_to_count, key=values_to_count.get)

        # Return the sorted list of values
        return sorted_values


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Cria uma lista de todas as variáveis ​​não atribuídas
        unassigned_variables = [var for var in self.crossword.variables if var not in assignment]

        # Classifica a lista de variáveis ​​não atribuídas pelo número de valores restantes em seus domínios
        unassigned_variables.sort(key=lambda var: len(self.domains[var]), reverse=False)

        # Se houver empate, classifique a lista de variáveis ​​​​empatadas pelo seu grau
        if len(unassigned_variables) > 1:
            unassigned_variables.sort(key=lambda var: len(self.crossword.neighbors(var)), reverse=True)

        # Retorna a primeira variável da lista ordenada
        return unassigned_variables[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Se todas as variáveis tiveram um valor atribuído retorne a atribuição
        if len(assignment) == len(self.crossword.variables):
            return assignment

        # Selecione uma variável não atribuída
        var = self.select_unassigned_variable(assignment)

        # Para cada valor no domínio da variável
        for value in var.domain:
            # Crie uma cópia da tarefa
            new_assignment = assignment.copy()

            # Atribua o valor á variável
            new_assignment[var] = value

            # Se a tarefa for consistente e completa, devolva-a
            if self.consistent(new_assignment) and self.assignment_complete(new_assignment):
                return new_assignment

            # Se a tarefa não for consistente ou completa, procure recursivamente por uma solução
            else:
                solution = self.backtrack(new_assignment)
                if solution is not None:
                    return solution

        # Se nenhum valor para a variável resultar em uma atribuição consistente e completa, retorne None
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
