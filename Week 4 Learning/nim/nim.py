import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Inicialize o tabuleiro do jogo.
        Cada tabuleiro de jogo tem
            - `pilhas`: uma lista de quantos elementos permanecem em cada pilha
            - `player`: 0 ou 1 para indicar a vez de qual jogador
            - `winner`: Nenhum, 0 ou 1 para indicar quem é o vencedor
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) recebe uma lista de `piles` como entrada
        e retorna todas as ações disponíveis `(i, j)` nesse estado.

        A ação `(i, j)` representa a ação de remover itens `j`
        da pilha `i` (onde as pilhas são indexadas em 0).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) retorna o player que não é
        `jogador`. Assume que `player` é 0 ou 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Mude o jogador atual para o outro jogador.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Faça o movimento `action` para o jogador atual.
        `action` deve ser uma tupla `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Inicialize a IA com um dicionário Q-learning vazio,
        uma taxa alfa (aprendizado) e uma taxa épsilon.

        O dicionário Q-learning mapeia `(estado, ação)`
        pares para um valor Q (um número).
         - `state` é uma tupla de pilhas restantes, por ex. (1, 1, 4, 4)
         - `action` é uma tupla `(i, j)` para uma ação
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Atualizar o modelo Q-learning, dado um estado antigo, uma ação tomada
        nesse estado, um novo estado resultante, e a recompensa recebida
        de tomar essa ação.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Retorne o valor Q para o estado `state` e a ação `action`.
        Se ainda não existir nenhum valor Q em `self.q`, retorne 0.
        """

        # Cria uma chave a partir do estado atual (convertido em tupla) e da ação
        key = (tuple(state), action)

        # Tenta retornar o valor Q correspondente, ou 0 se a chave não existir
        try:
            return self.q[key]
        except KeyError:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Atualize o valor Q para o estado `state` e a ação `action`
        dado o valor Q anterior `old_q`, uma recompensa atual `reward`,
        e uma estimativa de recompensas futuras `future_rewards`.

        Use a fórmula:

        Q(s, a) <- estimativa de valor antigo
                   + alfa * (nova estimativa de valor - estimativa de valor antiga)

        onde `estimativa de valor antigo` é o valor Q anterior,
        `alfa` é a taxa de aprendizagem e `nova estimativa de valor`
        é a soma da recompensa atual e das recompensas futuras estimadas.
        """

        # Cria uma chave a partir do estado atual (convertido em tupla) e da ação
        key = (tuple(state), action)

        # Obtém o valor Q antigo, definindo-o como 0 se a chave não existir
        old_q = self.q.setdefault(key, 0)

        # Calcula o novo valor Q usando a fórmula de atualização do Q-learning
        new_q_value = old_q + self.alpha * ((reward + future_rewards) - old_q)

        # Atualiza o valor Q na tabela Q com a nova chave e o novo valor Q
        self.q[key] = new_q_value

    def best_future_reward(self, state):
        """
        Dado um estado `estado`, considere todos os `(estado, ação)` possíveis
        pares disponíveis naquele estado e retorna o máximo de todos
        dos seus valores Q.

        Use 0 como valor Q se um par `(estado, ação)` não tiver
        Valor Q em `self.q`. Se não houver ações disponíveis em
        `estado`, retorne 0.
        """

        # Obtém todas as ações possíveis para o estado atual do jogo Nim
        possible_move = Nim.available_actions(state)

        # Se não houver ações possíveis, retorna 0 (fim do jogo)
        if not possible_move:
            return 0

        # Calcula os valores Q para todas as ações possíveis e retorna o máximo, ou -inf se a lista estiver vazia
        max_value = max((self.get_q_value(state, action) for action in possible_move), default=-float('inf'))

        # Retorna o maior valor Q encontrado
        return max_value

    def choose_action(self, state, epsilon=True):
        """
        Dado um estado `state`, retorne uma ação `(i, j)` a ser executada.

        Se `epsilon` for `False`, então retorne a melhor ação
        disponível no estado (aquele com maior valor Q,
        usando 0 para pares que não possuem valores Q).

        Se `epsilon` for `True`, então com probabilidade
        `self.epsilon` escolha uma ação aleatória disponível,
        caso contrário, escolha a melhor ação disponível.

        Se múltiplas ações tiverem o mesmo valor Q, qualquer uma delas
        options é um valor de retorno aceitável.
        """
        # Obtém todas as ações possíveis para o estado atual do jogo Nim
        possible_actions = Nim.available_actions(state)

        # Se não houver ações possíveis, retorna None (fim do jogo ou estado inválido)
        if not possible_actions:
            return None

        # Se a exploração estiver ativada (epsilon > 0) e um número aleatório entre 0 e 1 for menor que epsilon,
        # escolhe aleatoriamente uma ação das ações possíveis (exploração)
        if epsilon and random.uniform(0, 1) < self.epsilon:
            return random.choice(list(possible_actions))

        # Cria um dicionário de valores Q para todas as ações possíveis
        q_values = {action: self.get_q_value(state, action) for action in possible_actions}

        # Encontra a ação com o maior valor Q (ação ótima)
        best_action = max(q_values, key=q_values.get)

        # Retorna a melhor ação encontrada
        return best_action


def train(n):
    """
    Treine uma IA jogando `n` partidas contra ela mesma.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Jogue um jogo humano contra a IA.
    `human_player` pode ser definido como 0 ou 1 para especificar se
    o jogador humano se move primeiro ou segundo.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return
