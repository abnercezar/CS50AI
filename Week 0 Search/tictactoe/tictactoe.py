"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[None, None, None], [None, None, None], [None, None, None]]


# A player função deve receber um tabuleiro estado como entrada e retornar qual é a vez do jogador (ou X ou O).
def player(board):
    countX = 0
    countO = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX += 1
            if board[row][col] == O:
                countO += 1

    if countX > countO:
        return O
    else:
        return X


# A actions função deve retornar uma lista set de todas as ações possíveis que podem ser executadas em um determinado quadro.
def actions(board):
    allpossible_actions = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                allpossible_actions.add((row, col))
    return allpossible_actions


# A result função recebe o 'tabuleiro' e a ação como entrada e deve retornar um novo estado da placa, sem modificar a placa original.
def result(board, action):
    if action not in actions(board):
        raise Exception("Ação inválida")
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy


# A winner função deve aceitar o 'tabuleiro' como entrada e retornar o vencedor do 'tabuleiro', se houver.
def winner(board):
    if (
        checkRows(board, X)
        or checkColumns(board, X)
        or checkFirstDiag(board, X)
        or checkSecDiag(board, X)
    ):
        return X
    elif (
        checkRows(board, O)
        or checkColumns(board, O)
        or checkFirstDiag(board, O)
        or checkSecDiag(board, O)
    ):
        return O
    else:
        return None


# A terminal função deve aceitar o 'tabuleiro' como entrada e retornar um valor booleano indicando se o jogo acabou.
def terminal(board):
    return winner(board) is not None or all(
        all(cell != EMPTY for cell in row) for row in board
    )


# A utility função deve aceitar um terminal 'tabuleiro' como entrada e saída da utilidade da placa.
def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


# Esta função implementa a parte Max do algoritmo Minimax com poda Alfa-Beta.
def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


# Esta função implementa a parte Min do algoritmo Minimax com poda Alfa-Beta.
def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


# A minimax função deve receber o 'tabuleiro' como entrada e retornar o movimento ideal para o jogador se mover naquele 'tabuleiro'.
def minimax(board):
    if terminal(board):
        return None

    if player(board) == X:
        best_score = -math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = min_value(new_board, -math.inf, math.inf)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action
    else:
        best_score = math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = max_value(new_board, -math.inf, math.inf)
            if score < best_score:
                best_score = score
                best_action = action
        return best_action


# Esta função verifica se um jogador ganhou preenchendo uma linha inteira no 'tabuleiro'.
def checkRows(board, player):
    return any(row.count(player) == len(row) for row in board)


# Esta função verifica se um jogador ganhou preenchendo as colunas
def checkColumns(board, player):
    return any(col.count(player) == len(col) for col in zip(*board))


# Esta função verifica se um jogador ganhou preenchendo as diagonais do 'tabuleiro'.
# Verifique a diagonal principal
def checkFirstDiag(board, player):
    return board[0][0] == player and board[1][1] == player and board[2][2] == player


# Verifique a diagonal secundária
def checkSecDiag(board, player):
    return board[0][2] == player and board[1][1] == player and board[2][0] == player
