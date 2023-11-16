from move_handler import MoveHandler
from pawn import Pawn
from checkers_agent import CheckersAgent
import board_evaluator


class AgentMoveHandler(MoveHandler):

    def __init__(self, difficulty):
        super().__init__()
        self.agent = CheckersAgent()
        self.max_depth = None
        self.difficulty = None
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "EASY":
            self.max_depth = 1
        elif difficulty == "MEDIUM":
            self.max_depth = 3
        else:
            self.max_depth = 5

    def play(self, board, ui):
        depth = 0
        team = board.white_team

        pawns_and_captures = self.find_pawns_with_capture_moves(board, team)
        # Capture possible
        if pawns_and_captures:
            self.play_capture(board, pawns_and_captures, depth, ui)
        # No captures possible
        else:
            pawns_and_moves = self.find_pawns_with_moves(board, team)
            pawn, next_square_number = self.find_best_move(board, pawns_and_moves, depth, ui)
            self.move(board, pawn, next_square_number, ui)

    def find_best_move(self, board, pawns_and_moves, depth, ui):
        best_move_score = float('-inf')
        pawn_with_best_move = None
        best_move_square = None

        for pawn, next_possible_square_numbers in pawns_and_moves.items():
            for next_square_number in next_possible_square_numbers:
                alpha = float('-inf')  # Initialize alpha to negative infinity
                beta = float('inf')  # Initialize beta to positive infinity

                board_copy, _ = self.make_move_copy(board, pawn, next_square_number, is_capture=False, ui=ui)
                move_score = self.minimax(board_copy, depth + 1, alpha, beta, is_maximizing_turn=False, ui=ui)

                best_move_score, pawn_with_best_move, best_move_square = self.update_best_move(best_move_score,
                                                                                               move_score, pawn,
                                                                                               next_square_number,
                                                                                               pawn_with_best_move,
                                                                                               best_move_square)

        return pawn_with_best_move, best_move_square

    def play_capture(self, board, pawns_and_captures, depth, ui):
        pawn, jump_square_number = self.find_best_capture_move(board, pawns_and_captures, depth, ui)

        self.eat(board, pawn, jump_square_number, ui)

        next_jumping_squares = pawn.get_next_jumping_squares(board)
        if next_jumping_squares:
            pawns_and_captures = {pawn: next_jumping_squares}
            self.play_capture(board, pawns_and_captures, depth, ui)

    def find_best_capture_move(self, board, pawns_and_captures, depth, ui):
        best_capture_move_score = float('-inf')
        pawn_with_best_capture_move = None
        best_jump_square = None

        for pawn, possible_jump_square_numbers in pawns_and_captures.items():
            for jump_square_number in possible_jump_square_numbers:
                alpha = float('-inf')  # Initialize alpha to negative infinity
                beta = float('inf')  # Initialize beta to positive infinity

                board_copy, pawn_copy = self.make_move_copy(board, pawn, jump_square_number, is_capture=True, ui=ui)
                next_jumping_squares = pawn_copy.get_next_jumping_squares(board_copy)

                capture_move_score = self.get_move_score(board_copy, depth, alpha, beta, pawn_copy,
                                                         next_jumping_squares, is_maximizing_turn=True, ui=ui)

                best_capture_move_score, pawn_with_best_capture_move, best_jump_square = self.update_best_move(
                    best_capture_move_score,
                    capture_move_score, pawn,
                    jump_square_number,
                    pawn_with_best_capture_move,
                    best_jump_square)

        return pawn_with_best_capture_move, best_jump_square

    @staticmethod
    def update_best_move(best_move_score, move_score, pawn, next_square_number, pawn_with_best_move,
                         best_move_square):
        if move_score > best_move_score:
            return move_score, pawn, next_square_number
        else:
            return best_move_score, pawn_with_best_move, best_move_square

    def minimax(self, board, depth, alpha, beta, is_maximizing_turn, ui,
                is_consecutive_capture=False, capturing_pawn=None):
        # Base case
        if self.is_terminal_node(board, depth):
            return self.evaluate_board(board)

        team, best_move_score = self.initialize_minimax_variables(is_maximizing_turn, board)
        pruned = False

        pawns_and_captures = self.get_pawns_and_captures(board, team, is_consecutive_capture, capturing_pawn)
        if pawns_and_captures:
            for pawn, possible_jump_square_numbers in pawns_and_captures.items():
                for jump_square_number in possible_jump_square_numbers:
                    board_copy, pawn_copy = self.make_move_copy(board, pawn, jump_square_number, is_capture=True, ui=ui)
                    next_jumping_squares = pawn_copy.get_next_jumping_squares(board_copy)

                    move_score = self.get_move_score(board_copy, depth, alpha, beta, pawn_copy, next_jumping_squares,
                                                     is_maximizing_turn, ui)
                    best_move_score = self.update_best_move_score(is_maximizing_turn, best_move_score, move_score)

                    if is_maximizing_turn:
                        alpha = max(alpha, move_score)
                    else:
                        beta = min(beta, move_score)
                    if beta <= alpha:
                        pruned = True
                        break

                if pruned:
                    break

        # No possible captures
        else:
            pawns_and_moves = self.find_pawns_with_moves(board, team)
            for pawn, next_possible_square_numbers in pawns_and_moves.items():
                for next_square_number in next_possible_square_numbers:
                    board_copy, pawn_copy = self.make_move_copy(board, pawn, next_square_number, is_capture=False,
                                                                ui=ui)
                    move_score = self.get_move_score(board_copy, depth, alpha, beta, pawn_copy, None,
                                                     is_maximizing_turn, ui)
                    best_move_score = self.update_best_move_score(is_maximizing_turn, best_move_score, move_score)

                    if is_maximizing_turn:
                        alpha = max(alpha, move_score)
                    else:
                        beta = min(beta, move_score)
                    if beta <= alpha:
                        pruned = True
                        break

                if pruned:
                    break

        return best_move_score

    def is_terminal_node(self, board, depth):
        return (depth == self.max_depth or
                self.is_losing_team(board, board.black_team) or
                self.is_losing_team(board, board.white_team))

    @staticmethod
    def initialize_minimax_variables(is_maximizing_turn, board):
        if is_maximizing_turn:
            team = board.white_team
            best_move_score = float('-inf')
        else:
            team = board.black_team
            best_move_score = float('inf')
        return team, best_move_score

    def get_pawns_and_captures(self, board, team, is_consecutive_capture, capturing_pawn):
        if is_consecutive_capture:
            next_jumping_squares = capturing_pawn.get_next_jumping_squares(board)
            pawns_and_captures = {capturing_pawn: next_jumping_squares}
        else:
            pawns_and_captures = self.find_pawns_with_capture_moves(board, team)
        return pawns_and_captures

    def make_move_copy(self, board, pawn, next_square_number, is_capture, ui):
        board_copy = board.copy()
        pawn_copy = board_copy.get_occupying_pawn(pawn.square_number)
        if is_capture:
            opponent_square_number = Pawn.compute_opponent_square_number(pawn_copy.square_number, next_square_number)
            self.delete_opponent_pawn(board_copy, opponent_square_number, ui)
        self.update_move(board_copy, pawn_copy, next_square_number, ui)
        return board_copy, pawn_copy

    def get_move_score(self, board_copy, depth, alpha, beta, pawn, next_jumping_squares, is_maximizing_turn, ui):
        if next_jumping_squares:
            return self.minimax(board_copy, depth, alpha, beta, is_maximizing_turn, ui, is_consecutive_capture=True,
                                capturing_pawn=pawn)
        else:
            return self.minimax(board_copy, depth + 1, alpha, beta, is_maximizing_turn=not is_maximizing_turn, ui=ui)

    @staticmethod
    def update_best_move_score(is_maximizing_turn, best_move_score, move_score):
        if is_maximizing_turn:
            return max(best_move_score, move_score)
        else:
            return min(best_move_score, move_score)

    def evaluate_board(self, board, reverse=False):
        deserialized_board = board.deserialize()
        if reverse:
            deserialized_board = board_evaluator.reverse(deserialized_board)
        board_eval = board_evaluator.get_metrics(deserialized_board)
        move_score = self.agent.predict(board_eval)
        return move_score

    def offer_draw(self, board):
        agent_pos_eval = self.evaluate_board(board)
        human_pos_eval = self.evaluate_board(board, reverse=True)
        if (human_pos_eval - agent_pos_eval > 0.3 or
                (abs(agent_pos_eval - human_pos_eval) <= 0.1 and len(board.black_team) == len(board.white_team) == 1)):
            return True

        return False
