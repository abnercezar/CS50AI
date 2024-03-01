import itertools
import random


class Minesweeper:
    """
    Representação do jogo Campo Minado
    """

    # Este método inicializa o tabuleiro do Campo Minado com a altura e largura fornecidas e configura um campo minado vazio.
    def __init__(self, height=8, width=8, mines=8):
        # Definir largura inicial, altura e número de minas
        self.height = height
        self.width = width
        self.mines = set()

        # Inicializa um campo vazio sem minas
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Adicione minas aleatoriamente
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # A princípio, o jogador não encontrou nenhuma mina
        self.mines_found = set()

    def print(self):
        """
        Imprime uma representação baseada em texto
        de onde as minas estão localizadas.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        if i >= 0 and i < len(self.board) and j >= 0 and j < len(self.board[i]):
            return self.board[i][j]
        else:
            return False

    def nearby_mines(self, cell):
        """
        Retorna o número de minas que estão
        dentro de uma linha e coluna de uma determinada célula,
        não incluindo a própria célula.
        """

        # Mantenha a contagem das minas próximas
        count = 0

        # Loop sobre todas as células dentro de uma linha e coluna
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore a própria célula
                if (i, j) == cell:
                    continue

                # Atualizar contagem se a célula estiver dentro dos limites e for minha
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Verifica se todas as minas foram sinalizadas.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Declaração lógica sobre um jogo Campo Minado
    Uma frase consiste em um conjunto de células de tabuleiro,
    e uma contagem do número dessas células que são minas.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Retorna o conjunto de todas as células em self.cells conhecidas como minas.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Retorna um conjunto de todas as células conhecidas como seguras.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Atualiza a representação interna do conhecimento dado o fato de que
        uma célula é conhecida por ser uma mina.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Atualiza a representação interna do conhecimento dado o fato de que
        uma célula é conhecida por ser segura.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def update(self, marked_cell):
        """
        Remove a célula marcada da contagem da frase
        """
        # Remove a célula marcada da contagem da frase
        if marked_cell in self.cells:
            self.cells.remove(marked_cell)
            self.count -= 1

class MinesweeperAI:
    """
    Jogador do jogo Campo Minado
    """

    def __init__(self, height=8, width=8):
        # Definir altura e largura iniciais
        self.height = height
        self.width = width
        self.count = {}

        # Acompanhe quais células foram clicadas
        self.moves_made = set()

        # Acompanhe as células consideradas seguras ou minas
        self.mines = set()
        self.safes = set()

        # Lista de frases sobre o jogo conhecidas como verdadeiras
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marca uma célula como mina e atualiza todo o conhecimento
        para marcar aquela célula como uma mina também
        """
        # Verifica se a célula pode ser marcada como mina
        if self.can_mark_as_mine(cell):
            # Marca a célula como mina
            self.mines.add(cell)
            # Atualiza a base de conhecimento
            for sentence in self.knowledge:
                sentence.update(cell)
            # Retorna True indicando que a célula foi marcada com sucesso
            return True
        else:
            # Retorna False indicando que a célula não pôde ser marcada
            return False



    def mark_safe(self, cell):
        """
        Marca uma célula como segura e atualiza todo o conhecimento
        para marcar essa célula como segura também.
        """
        # Adiciona a célula à lista de células seguras
        self.safes.add(cell)

        # Itera sobre todas as sentenças conhecidas e marca a célula como segura nelas
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def can_mark_as_mine(self, cell):
       """
       Verifica se a célula pode ser marcada como mina com base no conhecimento atual
       """
       # Verifica se a célula ainda não foi marcada como mina
       if cell not in self.mines:
           # Verifica se a célula ainda está na contagem
           if cell in self.count:
               # Retorna True indicando que a célula pode ser marcada como mina
               return True
       # Retorna False indicando que a célula não pode ser marcada como mina
       return False

    def add_knowledge(self, cell, count):
        newSentence = None
        self.count[cell] = count
        """
        Chamado quando o tabuleiro do Campo Minado nos informa, para um determinado
        célula segura, quantas células vizinhas contêm minas.

        Esta função deve:
            1) marque a célula como um movimento que foi feito
            2) marque a célula como segura
            3) adicionar uma nova frase à base de conhecimento da IA
               com base no valor de `cell` e `count`
            4) marque quaisquer células adicionais como seguras ou como minas
               se puder ser concluído com base na base de conhecimento da IA
            5) adicionar novas frases à base de conhecimento da IA
               se eles podem ser inferidos a partir do conhecimento existente
        """
        # 1. Marca a célula como um movimento feito
        self.moves_made.add(cell)

        # 2. Marca a célula como segura
        self.mark_safe(cell)

        undeterminedCells = []
        countMines = 0

        # 3. Verifica as células vizinhas
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) in self.mines:
                    countMines += 1

                # Adiciona células não determinadas à lista
                if (
                    0 <= i < self.height
                    and 0 <= j < self.width
                    and (i, j) not in self.safes
                    and (i, j) not in self.mines
                ):
                    undeterminedCells.append((i, j))

        # 4. Adiciona uma nova sentença à base de conhecimento do AI
        if len(undeterminedCells) >= count - countMines:
            newSentence = Sentence(undeterminedCells, count - countMines)

            # Itera sobre as células não determinadas e verifica se pode inferir minas
            for cell in undeterminedCells:
                if cell not in self.safes and cell not in self.mines:
                    # Verifica se a célula pode ser inferida como uma mina com base na base de conhecimento
                    if all(sentence.mark_mine(cell) for sentence in self.knowledge):
                        self.mines.add(cell)



        # Atualiza a base de conhecimento com base na nova informação
        self.knowledge.append(newSentence)

        # 5. Marca as minas e células seguras conhecidas em todas as sentenças
        for sentence in self.knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

        # 6. Verifica se uma sentença é um subconjunto de outra e cria uma nova sentença
        for sentence in self.knowledge:
            if (
                newSentence.cells.issubset(sentence.cells)
                and sentence.count > 0
                and newSentence.count > 0
                and newSentence != sentence
            ):
                newSubset = sentence.cells.difference(newSentence.cells)
                newSentenceSubset = Sentence(
                    list(newSubset), sentence.count - newSentence.count
                )
                self.knowledge.append(newSentenceSubset)

    def make_safe_move(self):
        """
        Retorna uma célula segura para escolher no tabuleiro do Campo Minado.
        A mudança deve ser considerada segura e não já uma mudança
        que foi feito.

        Esta função pode usar o conhecimento em self.mines, self.safes
        e self.moves_made, mas não deve modificar nenhum desses valores.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Retorna um movimento a ser feito no tabuleiro do Campo Minado.
        Deve escolher aleatoriamente entre células que:
            1) ainda não foram escolhidos, e
            2) não são conhecidos por serem minas
        """
        possibleMoves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possibleMoves.append((i, j))
        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None
