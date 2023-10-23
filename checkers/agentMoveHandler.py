import sys
from moveHandler import MoveHandler
from board import Board

sys.path.append('agent') 
import checkers_agent 
import boardEvaluator

class AgentMoveHandler(MoveHandler):

    def __init__(self):
        self.agent = checkers_agent.CheckersAgent()
    
    def play(self, board):
        blue_pawns_and_captures = self.findPawnsWithCaptureMoves(board, board.blue_team)
        if blue_pawns_and_captures:
            self.playCapture(board, blue_pawns_and_captures)
        # No captures possible
        else:
            blue_pawns_and_moves = self.findPawnsWithMoves(board, board.blue_team)
            pawn, next_square_number = self.findBestMove(board, blue_pawns_and_moves)
            self.move(board, pawn, next_square_number)

    def playCapture(self, board, blue_pawns_and_captures):
        pawn, jump_square_number = self.findBestCaptureMove(board, blue_pawns_and_captures)
        self.eat(board, pawn, jump_square_number)

        next_jumping_squares = pawn.getNextJumpingSquares(board)
        if next_jumping_squares:
            blue_pawns_and_captures = {pawn: next_jumping_squares}
            self.playCapture(board, blue_pawns_and_captures)

    def findBestCaptureMove(self, board, pawns_and_captures):
        pawn_with_best_capture = None
        best_jump_square = None
        best_capture_score = float('-inf')
        deserialized_board = board.deserialize()

        for pawn, possible_jump_square_numbers in pawns_and_captures.items():
            for jump_square_number in possible_jump_square_numbers:
                capture_score = self.computeMoveScore(deserialized_board, pawn.square_number, jump_square_number, is_capture=True)
                if capture_score > best_capture_score:
                    pawn_with_best_capture = pawn
                    best_jump_square = jump_square_number
                    best_capture_score = capture_score

        return pawn_with_best_capture, best_jump_square
    
    def findPawnsWithMoves(self, board, pawn_team):
        """
        Returns a dictionary where keys are pawns,
        and values are corresponding sets of the pawn's next possible squares
        """
        pawns_and_moves = {}
        for pawn in pawn_team:
            next_squares = pawn.getNextSquares(board)
            if next_squares:
                pawns_and_moves[pawn] = next_squares
        return pawns_and_moves 
    
    def findBestMove(self, board, pawns_and_moves):
        pawn_with_best_move = None
        best_move_square = None
        best_move_score = float('-inf')
        deserialized_board = board.deserialize()

        for pawn, next_possible_square_numbers in pawns_and_moves.items():
            for square_number in next_possible_square_numbers:
                move_score = self.computeMoveScore(deserialized_board, pawn.square_number, square_number, is_capture=False)
                if move_score > best_move_score:
                    pawn_with_best_move = pawn
                    best_move_square = square_number
                    best_move_score = move_score

        return pawn_with_best_move, best_move_square
    
    def computeMoveScore(self, deserialized_board, start_square, end_square, is_capture):
        updated_deserialized_board = Board.play_move_on_deserialized_board(deserialized_board, start_square, end_square, is_capture)
        board_eval = boardEvaluator.get_metrics(updated_deserialized_board).reshape(1, -1)
        move_score = self.agent.predict(board_eval)
        return move_score