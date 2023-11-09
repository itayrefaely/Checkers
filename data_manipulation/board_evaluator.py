import numpy as np


# American checkers: wikipedia.org/wiki/English_draughts
# on a 8x8 checkerboard, both players start with 12 men
# Black plays the first move
# all pieces can only move and capture diagonally
# men can only move/capture diagonally forward
# kings can move/capture in any diagonal direction
# if a man reaches the other side of the board, the turn ends, and it becomes a king
# captures are made by moving any piece diagonally over an opponent's
# if a capture can be made, it must be taken
# multiple captures can be made in a single turn and with a single piece
# the game ends when a player captures all the opponent's pieces
# a player also wins when the opponent can not make a legal move

# example board:
# /b/b/b/b	b/w = Black/White man {1, -1}
# b/b/b/b/	B/W = Black/White king {3, -3}
# /b/b/b/b	_ = empty square {0}
# _/_/_/_/	/ = unusable square
# /_/_/_/_
# w/w/w/w/
# /w/w/w/w
# w/w/w/w/	* since pieces only move diagonally, only 32 squares are used

# number of opponent pieces captured (max = 12)
def num_captured(board):
    return 12 - np.sum(board < 0)


def num_branches(board, x, y):
    count = 0
    if board[x, y] >= 1 and x < 6:
        if y < 6:
            if board[x + 1, y + 1] < 0 and board[x + 2, y + 2] == 0:
                board[x + 2, y + 2] = board[x, y]
                board[x, y] = 0
                temp = board[x + 1, y + 1]
                board[x + 1, y + 1] = 0
                count += num_branches(board, x + 2, y + 2) + 1
                board[x + 1, y + 1] = temp
                board[x, y] = board[x + 2, y + 2]
                board[x + 2, y + 2] = 0
        if y > 1:
            if board[x + 1, y - 1] < 0 and board[x + 2, y - 2] == 0:
                board[x + 2, y - 2] = board[x, y]
                board[x, y] = 0
                temp = board[x + 1, y - 1]
                board[x + 1, y - 1] = 0
                count += num_branches(board, x + 2, y - 2) + 1
                board[x + 1, y - 1] = temp
                board[x, y] = board[x + 2, y - 2]
                board[x + 2, y - 2] = 0
    if board[x, y] == 3 and x > 0:
        if y < 6:
            if board[x - 1, y + 1] < 0 and board[x - 2, y + 2] == 0:
                board[x - 2, y + 2] = board[x, y]
                board[x, y] = 0
                temp = board[x - 1, y + 1]
                board[x - 1, y + 1] = 0
                count += num_branches(board, x - 2, y + 2) + 1
                board[x - 1, y + 1] = temp
                board[x, y] = board[x - 2, y + 2]
                board[x - 2, y + 2] = 0
        if y > 1:
            if board[x - 1, y - 1] < 0 and board[x - 2, y - 2] == 0:
                board[x - 2, y - 2] = board[x, y]
                board[x, y] = 0
                temp = board[x - 1, y - 1]
                board[x - 1, y - 1] = 0
                count += num_branches(board, x - 2, y - 2) + 1
                board[x - 1, y - 1] = temp
                board[x, y] = board[x - 2, y - 2]
                board[x - 2, y - 2] = 0
    return count


def possible_moves(board):
    count = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i, j] > 0:
                count += num_branches(board, i, j)
    if count > 0:
        return count
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i, j] >= 1 and i < 7:
                if j < 7:
                    count += (board[i + 1, j + 1] == 0)
                if j > 0:
                    count += (board[i + 1, j - 1] == 0)
            if board[i, j] == 3 and i > 0:
                if j < 7:
                    count += (board[i - 1, j + 1] == 0)
                elif j > 0:
                    count += (board[i - 1, j - 1] == 0)
    return count


def game_winner(board):
    if np.sum(board < 0) == 0:
        return 1
    elif np.sum(board > 0) == 0:
        return -1
    if possible_moves(board) == 0:
        return -1
    elif possible_moves(reverse(board)) == 0:
        return 1
    else:
        return 0


def at_enemy(board):
    count = 0
    for i in range(5, 8):
        count += np.sum(board[i] == 1) + np.sum(board[i] == 3)
    return count


def at_middle(board):
    count = 0
    for i in range(3, 5):
        count += np.sum(board[i] == 1) + np.sum(board[i] == 3)
    return count


def num_men(board):
    return np.sum(board == 1)


def num_kings(board):
    return np.sum(board == 3)


def capturables(board):  # possible number of unsupported enemies
    count = 0
    for i in range(1, 7):
        for j in range(1, 7):
            if board[i, j] < 0:
                count += (board[i + 1, j + 1] >= 0 and board[i + 1, j - 1] >= 0 and board[i - 1, j + 1] >= 0 and board[
                    i - 1, j - 1] >= 0)
    return count


def semicapturables(board):  # number of own units with at least one support
    return 12 - uncapturables(board) - capturables(reverse(board))


def uncapturables(board):  # number of own units that can't be captured
    count = 0
    for i in range(1, 7):
        for j in range(1, 7):
            if board[i, j] > 0:
                count += ((board[i + 1, j + 1] > 0 < board[i + 1, j - 1]) or (
                        board[i - 1, j + 1] > 0 < board[i - 1, j - 1]) or (
                                  board[i + 1, j + 1] > 0 < board[i - 1, j + 1]) or (
                                  board[i + 1, j - 1] > 0 < board[i - 1, j - 1]))
    count += np.sum(board[0] == 1) + np.sum(board[0] == 3) + np.sum(board[1:7, 0] == 1) + np.sum(
        board[1:7, 0] == 3) + np.sum(board[7] == 1) + np.sum(board[7] == 3) + np.sum(board[1:7, 7] == 1) + np.sum(
        board[1:7, 7] == 3)
    return count


def reverse(board):
    b = -board
    b = np.fliplr(b)
    b = np.flipud(b)
    return b


def get_metrics(board):  # returns [label, 10 labeling metrics]
    b = board

    capped = num_captured(b)
    potential = possible_moves(b) - possible_moves(reverse(b))
    men = num_men(b) - num_men(-b)
    kings = num_kings(b) - num_kings(-b)
    caps = capturables(b) - capturables(reverse(b))
    semicaps = semicapturables(b)
    uncaps = uncapturables(b) - uncapturables(reverse(b))
    mid = at_middle(b) - at_middle(-b)
    far = at_enemy(b) - at_enemy(reverse(b))
    won = game_winner(b)

    score = 4 * capped + potential + men + 3 * kings + caps + 2 * semicaps + 3 * uncaps + 2 * mid + 3 * far + 100 * won

    return np.array([score, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])


def np_board():
    return np.array(get_board())


def get_board():
    return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]


def expand(board):
    b = np.zeros((8, 8), dtype='b')
    for i in range(0, 8):
        if i % 2 == 0:
            b[i] = np.array([0, board[i * 4], 0, board[i * 4 + 1], 0, board[i * 4 + 2], 0, board[i * 4 + 3]])
        else:
            b[i] = np.array([board[i * 4], 0, board[i * 4 + 1], 0, board[i * 4 + 2], 0, board[i * 4 + 3], 0])
    return b


def compress(board):
    b = np.zeros((1, 32), dtype='b')
    for i in range(0, 8):
        if i % 2 == 0:
            b[0, i * 4: i * 4 + 4] = np.array([board[i, 1], board[i, 3], board[i, 5], board[i, 7]])
        else:
            b[0, i * 4: i * 4 + 4] = np.array([board[i, 0], board[i, 2], board[i, 4], board[i, 6]])
    return b
