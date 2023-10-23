import re
import sys
import numpy as np

sys.path.append('./agent') 
import boardEvaluator 

class GameParser():

    filename = "board_evals.csv"

    def __init__(self):
        self.board_array = np.array([
                                    [0, 1, 0, 1, 0, 1, 0, 1],
                                    [1, 0, 1, 0, 1, 0, 1, 0],
                                    [0, 1, 0, 1, 0, 1, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0],
                                    [-1, 0, -1, 0, -1, 0, -1, 0],
                                    [0, -1, 0, -1, 0, -1, 0, -1],
                                    [-1, 0, -1, 0, -1, 0, -1, 0]
                                    ])

    def parseGame(game_record):
        game_parser = GameParser()
        # Split the game_record string using any whitespace character
        game_record = re.split(r'\s+', game_record)
        game_outcome = GameParser.parseOutcome(game_record[-1])

        for i in range(0, len(game_record) - 1, 3):
            black_move, white_move = game_record[i+1], game_record[i+2]

            if black_move == game_record[-1]:
                break
            game_parser.parseMove(black_move)
            game_parser.evaluateAndAddToFile(game_outcome, reverse=False)

            if white_move == game_record[-1]:
                break
            game_parser.parseMove(white_move)
            game_parser.evaluateAndAddToFile(game_outcome, reverse=True)

    def parseMove(self, move):
        if 'x' in move:
            self.parseCaptureMove(move)
        else:
            move = move.split('-')
            start_square, end_square = int(move[0]), int(move[1])
            start_square, end_square = self.expandSquare(start_square), self.expandSquare(end_square) 
            self.updateMove(start_square, end_square)

    def parseCaptureMove(self, move):
        move = move.split('x')
        # delete captured opponents
        for i in range(len(move)):
            move[i] = self.expandSquare(move[i]) 
        for idx, square_one in enumerate(move[:-1]):
            square_two = move[idx + 1]
            capture_square = (square_one + square_two) / 2
            capture_row, capture_col = self.computeRowAndCol(capture_square)
            self.board_array[capture_row, capture_col] = 0

        # move pawn
        start_square, end_square = int(move[0]), int(move[-1])
        self.updateMove(start_square, end_square)

    def computeRowAndCol(self, square_number):
        """"
        Returns row, col indeces (between 0 and 7 inclusive)
        """
        square_number = int(square_number)
        row = (square_number - 1) // 8
        col = (square_number - 1) % 8
        return row, col
        
    def updateMove(self, start_square, end_square):
        start_row, start_col = self.computeRowAndCol(start_square)
        end_row, end_col = self.computeRowAndCol(end_square)

        prev_pawn_value = self.board_array[start_row, start_col]
        cur_pawn_value = self.getPawnValue(prev_pawn_value, end_square)

        # Update move in the board
        self.board_array[start_row, start_col] = 0
        self.board_array[end_row, end_col] = cur_pawn_value

    def getPawnValue(self, prev_pawn_value, end_square):
        # end_square is a promotion square
        if (prev_pawn_value == 1 and 57 <= end_square <= 64) or \
            (prev_pawn_value == -1 and 1 <= end_square <= 8):
            return 3 * prev_pawn_value
        
        return prev_pawn_value
    
    def evaluateAndAddToFile(self, game_outcome, reverse):
        board = self.board_array
        outcome = game_outcome
        if reverse:
            board = boardEvaluator.reverse(board)
            outcome = -1 * outcome

        arr = boardEvaluator.get_metrics(board)
        arr = np.append(arr, outcome)
        arr_str = np.array2string(arr, separator=',', max_line_width=np.inf)
        cleaned_str = re.sub(r'\s+|\[|\]', '', arr_str)

        with open(GameParser.filename, "a") as file:
            # Add a new line to the file
            file.write(cleaned_str + '\n')

    def parseOutcome(game_outcome):
        if game_outcome == '0-1':
            res = -1
        elif game_outcome == '1/2-1/2':
            res = 0
        else:
            res = 1
        
        return res
    
    def expandSquare(self, square_number):
        square_number = int(square_number)
        # Odd row 
        if 1 <= (square_number % 8) <= 4:
            return int(2 * square_number)
        # Even row
        return int(2 * square_number - 1)