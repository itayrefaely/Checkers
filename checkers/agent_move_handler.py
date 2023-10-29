from move_handler import MoveHandler
from pawn import Pawn
from checkers_agent import CheckersAgent
import board_evaluator
from queen import Queen

class AgentMoveHandler(MoveHandler):

    def __init__(self):
        self.agent = CheckersAgent()
        self.max_depth = 3
    
    def play(self, board):
        depth = 0
        team = board.blue_team

        pawns_and_captures = self.find_pawns_with_capture_moves(board, team)
        # Capture possible
        if pawns_and_captures:
            self.play_capture(board, pawns_and_captures, depth)
        # No captures possible
        else:
            pawns_and_moves = self.find_pawns_with_moves(board, team)
            pawn, next_square_number = self.find_best_move(board, pawns_and_moves, depth)
            self.move(board, pawn, next_square_number)

    def find_best_move(self, board, pawns_and_moves, depth):
        best_move_score = float('-inf')
        # Can do similar if condition to play_capture
        pawn_with_best_move = None
        best_move_square = None

        for pawn, next_possible_square_numbers in pawns_and_moves.items():
            for next_square_number in next_possible_square_numbers:
                board_copy = board.copy()
                pawn_copy = board_copy.get_occupying_pawn(pawn.square_number)
                self.update_move(board_copy, pawn_copy, next_square_number)
                move_score = self.minimax(board_copy, depth + 1, is_maximizing_turn=False)

                if move_score > best_move_score:
                    best_move_score = move_score
                    pawn_with_best_move = pawn
                    best_move_square = next_square_number
        
        return pawn_with_best_move, best_move_square

    def play_capture(self, board, pawns_and_captures, depth):
        if len(pawns_and_captures) == 1:
            pawn = next(iter(pawns_and_captures))
            jump_square_number = pawns_and_captures[pawn].pop()

        else:
            pawn, jump_square_number = self.find_best_capture_move(board, pawns_and_captures, depth)

        self.eat(board, pawn, jump_square_number)

        next_jumping_squares = pawn.get_next_jumping_squares(board)
        if next_jumping_squares:
            pawns_and_captures = {pawn: next_jumping_squares}
            self.play_capture(board, pawns_and_captures, depth)

    def find_best_capture_move(self, board, pawns_and_captures, depth):
        best_capture_move_score = float('-inf')
        pawn_with_best_capture_move = None
        best_jump_square = None

        for pawn, possible_jump_square_numbers in pawns_and_captures.items():
            for jump_square_number in possible_jump_square_numbers:
                board_copy = board.copy()
                pawn_copy = board_copy.get_occupying_pawn(pawn.square_number)
                # Delete the opponent pawn
                opponent_square_number = Pawn.compute_opponent_square_number(pawn_copy.square_number, jump_square_number)
                self.delete_opponent_pawn(board_copy, opponent_square_number)

                self.update_move(board_copy, pawn_copy, jump_square_number)
                next_jumping_squares = pawn_copy.get_next_jumping_squares(board_copy)

                # Consecutive captures possible
                if next_jumping_squares:
                    capture_move_score = self.minimax(board_copy, depth, is_maximizing_turn=True, is_consecutive_capture=True, capturing_pawn=pawn_copy)
                # No consecutive captures
                else:
                    capture_move_score = self.minimax(board_copy, depth + 1, is_maximizing_turn=False)

                if capture_move_score > best_capture_move_score:
                    best_capture_move_score = capture_move_score
                    pawn_with_best_capture_move = pawn
                    best_jump_square = jump_square_number

        return pawn_with_best_capture_move, best_jump_square

    def minimax(self, board, depth, is_maximizing_turn, is_consecutive_capture=False, capturing_pawn=None):
        # Base case: check if the node is a terminal node (end of game or max depth)
        if depth == self.max_depth or self.is_losing_team(board, board.red_team) or self.is_losing_team(board, board.blue_team):
            return self.evaluate(board)
        
        if is_maximizing_turn:
            team = board.blue_team
            best_move_score = float('-inf')

            if is_consecutive_capture:
                next_jumping_squares = capturing_pawn.get_next_jumping_squares(board)
                pawns_and_captures = {capturing_pawn: next_jumping_squares}
            else:
                pawns_and_captures = self.find_pawns_with_capture_moves(board, team)

            if pawns_and_captures:
                for pawn, possible_jump_square_numbers in pawns_and_captures.items():
                    for jump_square_number in possible_jump_square_numbers:
                        board_copy = board.copy()
                        pawn_copy = board_copy.get_occupying_pawn(pawn.square_number) 
                        # Delete the opponent pawn
                        opponent_square_number = Pawn.compute_opponent_square_number(pawn_copy.square_number, jump_square_number)
                        self.delete_opponent_pawn(board_copy, opponent_square_number)

                        self.update_move(board_copy, pawn_copy, jump_square_number)
                        next_jumping_squares = pawn_copy.get_next_jumping_squares(board_copy)

                        # Consecutive captures possible
                        if next_jumping_squares:
                            move_score = self.minimax(board_copy, depth, is_maximizing_turn=True, is_consecutive_capture=True, capturing_pawn=pawn_copy)
                        # No consecutive captures
                        else:
                            move_score = self.minimax(board_copy, depth + 1, is_maximizing_turn=False)
                        
                        best_move_score = max(best_move_score, move_score)
            # No captures possible
            else:
                pawns_and_moves = self.find_pawns_with_moves(board, team)
                for pawn, next_possible_square_numbers in pawns_and_moves.items():
                    for next_square_number in next_possible_square_numbers:
                        board_copy = board.copy()
                        pawn_copy = board_copy.get_occupying_pawn(pawn.square_number) 
                        self.update_move(board_copy, pawn_copy, next_square_number)
                        move_score = self.minimax(board_copy, depth + 1, is_maximizing_turn=False)
                        best_move_score = max(best_move_score, move_score)
        # Minimizing turn
        else:
            team = board.red_team
            best_move_score = float('inf')

            if is_consecutive_capture:
                next_jumping_squares = capturing_pawn.get_next_jumping_squares(board)
                pawns_and_captures = {capturing_pawn: next_jumping_squares}
            else:
                pawns_and_captures = self.find_pawns_with_capture_moves(board, team)

            if pawns_and_captures:
                for pawn, possible_jump_square_numbers in pawns_and_captures.items():
                    for jump_square_number in possible_jump_square_numbers:
                        board_copy = board.copy()
                        pawn_copy = board_copy.get_occupying_pawn(pawn.square_number) 
                        # Delete the opponent pawn
                        opponent_square_number = Pawn.compute_opponent_square_number(pawn_copy.square_number, jump_square_number)
                        self.delete_opponent_pawn(board_copy, opponent_square_number)

                        self.update_move(board_copy, pawn_copy, jump_square_number)
                        next_jumping_squares = pawn_copy.get_next_jumping_squares(board_copy)

                        # Consecutive captures possible
                        if next_jumping_squares:
                            move_score = self.minimax(board_copy, depth, is_maximizing_turn=False, is_consecutive_capture=True, capturing_pawn=pawn_copy)
                        # No consecutive captures
                        else:
                            move_score = self.minimax(board_copy, depth + 1, is_maximizing_turn=True)
                        
                        best_move_score = min(best_move_score, move_score)
            # No captures possible
            else:
                pawns_and_moves = self.find_pawns_with_moves(board, team)
                for pawn, next_possible_square_numbers in pawns_and_moves.items():
                    for next_square_number in next_possible_square_numbers:
                        board_copy = board.copy()
                        pawn_copy = board_copy.get_occupying_pawn(pawn.square_number)
                        self.update_move(board_copy, pawn_copy, next_square_number)
                        move_score = self.minimax(board_copy, depth + 1, is_maximizing_turn=True)
                        best_move_score = min(best_move_score, move_score)

        return best_move_score
        
    def evaluate(self, board):
        deserialized_board = board.deserialize()
        board_eval = board_evaluator.get_metrics(deserialized_board).reshape(1, -1)

        return board_eval[0][0]
        # move_score = self.agent.predict(board_eval)
        # return move_score