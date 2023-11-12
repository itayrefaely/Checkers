import pygame
from square import Square
from pawn import Pawn


class MoveHandler:

    def __init__(self):
        self.is_player_turn = True

    def initialize_new_move(self, board):
        """
        Initializes a new move in the game.

        This method checks if any red pawns have capturing moves. If so, it highlights them.
        If there are no capturing moves, it highlights red pawns with possible moves.
        """
        red_pawns_with_capture = self.find_pawns_with_capture_moves(board, board.red_team)

        if red_pawns_with_capture:
            for pawn in red_pawns_with_capture.keys():
                pawn.highlight(board)
        else:
            self.highlight_pawns_with_possible_moves(board, board.red_team)

        pygame.display.flip()

    @staticmethod
    def find_pawns_with_capture_moves(board, pawn_team):
        """
        Returns a dictionary where keys are pawns,
        and values are corresponding sets of squares that the pawn can jump to after a capture.
        """
        pawns_and_captures = {}
        for pawn in pawn_team:
            possible_jumping_squares = pawn.get_next_jumping_squares(board)
            if possible_jumping_squares:
                pawns_and_captures[pawn] = possible_jumping_squares

        return pawns_and_captures

    @staticmethod
    def find_pawns_with_moves(board, pawn_team):
        """
        Returns a dictionary where keys are pawns,
        and values are corresponding sets of the pawn's next possible squares
        """
        pawns_and_moves = {}
        for pawn in pawn_team:
            next_squares = pawn.get_next_squares(board)
            if next_squares:
                pawns_and_moves[pawn] = next_squares

        return pawns_and_moves

    @staticmethod
    def highlight_pawns_with_possible_moves(board, pawn_team):
        for pawn in pawn_team:
            if pawn.get_next_squares(board):
                pawn.highlight(board)

    def is_legal_press(self, board, pos, is_first_press):
        """
        Determine if a press event is legal and handle it accordingly.

        Args:
            board (Board): The game board.
            pos (tuple): The mouse click position.
            is_first_press (bool): True if it's the first press, False for the second.

        Returns:
            bool: True if the press is legal and handled, False otherwise.
        """
        square_number = self.get_pressed_square(board, pos)
        # Check if the click was outside the board
        if not square_number:
            return False

        if is_first_press:
            return self.handle_first_press(board, square_number)
        else:
            return self.handle_second_press(board, square_number)

    def handle_first_press(self, board, square_number):
        """
        Handle the first press event.

        Args:
            board (Board): The game board.
            square_number (int): The square number that was pressed.

        Returns:
            bool: True if the first press is legal and handled, False otherwise.
        """
        chosen_pawn = self.find_chosen_pawn(board.red_team, square_number)

        if not chosen_pawn or not chosen_pawn.highlighted:
            return False

        next_squares = chosen_pawn.get_next_squares(board)
        if not next_squares:
            return False

        # Un-highlight all previously highlighted pawns and select the chosen pawn
        self.unhighlight_all(board, board.red_team)
        self.select(board, chosen_pawn, next_squares)
        return True

    def handle_second_press(self, board, square_number):
        """
        Handle the second press event.

        Args:
            board (Board): The game board.
            square_number (int): The square number that was pressed.

        Returns:
            bool: True if the second press is legal and handled, False otherwise.
        """
        chosen_pawn, prev_pawn = self.find_prev_and_cur_pawns(board.red_team, square_number)

        # Check if a red pawn was pressed again
        if chosen_pawn and prev_pawn:
            return self.handle_second_press_pawn(board, chosen_pawn, prev_pawn)

        # If pressed a selected square
        elif board.squares[square_number].selected:
            return self.handle_second_press_square(board, prev_pawn, square_number)

        return False

    def handle_second_press_pawn(self, board, chosen_pawn, prev_pawn):
        """
        Handle the second press event when a pawn is selected.

        Args:
            board (Board): The game board.
            chosen_pawn (Pawn): The newly chosen pawn.
            prev_pawn (Pawn): The previously chosen pawn.

        Returns:
            bool: True if the second press with a pawn is legal and handled, False otherwise.
        """
        # Same pawn
        if chosen_pawn == prev_pawn or prev_pawn.ate_this_turn:
            return False

        # If chosen a new pawn who has no capturing moves and the last pawn does have
        if prev_pawn.can_eat and not chosen_pawn.can_eat:
            return False

        # Legal choice of different pawn
        prev_next_squares = prev_pawn.get_next_squares(board)
        self.deselect(board, prev_pawn, prev_next_squares)

        next_squares = chosen_pawn.get_next_squares(board)
        # If the new pawn has no moving options, this press cancels the previous one
        if not next_squares:
            return True

        # Select the new pawn
        self.select(board, chosen_pawn, next_squares)
        return False

    def handle_second_press_square(self, board, prev_pawn, square_number):
        """
        Handle the second press event when a square is selected.

        Args:
            board (Board): The game board.
            prev_pawn (Pawn): The previously chosen pawn.
            square_number (int): The square number that was pressed.

        Returns:
            bool: True if the second press with a square is legal and handled, False otherwise.
        """
        # If an eating move
        if prev_pawn.can_eat:
            prev_next_squares = prev_pawn.get_next_squares(board)
            self.deselect(board, prev_pawn, prev_next_squares)
            self.eat(board, prev_pawn, square_number)

            next_jumping_squares = prev_pawn.get_next_jumping_squares(board)
            # Has more eating options
            if next_jumping_squares:
                prev_pawn.ate_this_turn = True
                self.select(board, prev_pawn, next_jumping_squares)
                return False
            # No more eating options
            else:
                prev_pawn.ate_this_turn = False
                self.is_player_turn = False
                return True
        # Not an eating move
        else:
            prev_next_squares = prev_pawn.get_next_squares(board)
            self.deselect(board, prev_pawn, prev_next_squares)
            self.move(board, prev_pawn, square_number)
            self.is_player_turn = False
            return True

    @staticmethod
    def get_pressed_square(board, pos):
        row, col = pos[1] // board.square_size, pos[0] // board.square_size + 1
        square_number = 8 * (row - 1) + col
        if square_number > 64 or square_number < 1:
            square_number = 0
        return square_number

    @staticmethod
    def find_chosen_pawn(pawn_team, square_number):
        """
        Find the chosen pawn among the given team.

        Returns:
            Pawn or None: The chosen pawn or None if not found.
        """
        for pawn in pawn_team:
            if pawn.square_number == square_number:
                return pawn
        return None

    @staticmethod
    def unhighlight_all(board, pawn_team):
        """
        Un-highlight all pawns in the specified list.
        """
        for pawn in pawn_team:
            if pawn.highlighted:
                pawn.unhighlight()
        board.draw()

    @staticmethod
    def find_prev_and_cur_pawns(pawn_team, square_number):
        """
        Find the previously and new chosen pawns

        Args:
            pawn_team (list): List of pawns to search in.
            square_number (int): The square number to search for.

        Returns: Tuple[Pawn, Pawn]: A tuple containing two pawns, one for the chosen square and one for the
        previously selected square.
        """
        chosen_pawn, prev_pawn = None, None
        for pawn in pawn_team:
            if pawn.square_number == square_number:
                chosen_pawn = pawn
            if pawn.selected:
                prev_pawn = pawn
        return chosen_pawn, prev_pawn

    @staticmethod
    def select(board, pawn, next_squares):
        # Select the pawn
        pawn.select(board)

        # Select the next possible squares
        for square_number in next_squares:
            square = board.squares[square_number]
            square.select(board, pawn.radius)

        pygame.display.flip()

    @staticmethod
    def deselect(board, pawn, next_squares):
        # Deselect the pawn
        pawn.deselect()

        # Deselect the next possible squares
        for square_number in next_squares:
            square = board.squares[square_number]
            square.deselect()

        board.draw()

    def move(self, board, pawn, next_square_number):
        """
        Move a pawn to a new square on the board.

        This method handles the pawn's movement animation and updating the pawn's position and square.

        Args:
            board (Board): The game board.
            pawn (Pawn): The pawn to be moved.
            next_square_number (int): The square number to move the pawn to.
        """
        clock = pygame.time.Clock()
        start_pos = pawn.center
        end_pos = board.squares[next_square_number].get_center()

        # Movement parameters
        duration = 200  # Duration of the movement in milliseconds
        start_time = pygame.time.get_ticks()

        self.animate_movement(board, pawn, start_pos, end_pos, duration, start_time, clock)

        # Update fields of pawn and its new square
        self.update_move(board, pawn, next_square_number)

    def eat(self, board, pawn, jump_square_number):
        """
        Move a pawn to a new square after capturing an opponent's pawn.

        This method handles the pawn's movement animation, removal of the captured
        opponent's pawn, and updating the pawn's position and square.

        Args:
            board (Board): The game board.
            pawn (Pawn): The pawn performing the capture move.
            jump_square_number (int): The square number to move the pawn to after capturing.
        """
        clock = pygame.time.Clock()
        start_pos = pawn.center
        end_pos = board.squares[jump_square_number].get_center()

        # Delete the opponent pawn
        opponent_square_number = Pawn.compute_opponent_square_number(pawn.square_number, jump_square_number)
        self.delete_opponent_pawn(board, opponent_square_number)

        # Movement parameters
        duration = 250  # Duration of the movement in milliseconds
        start_time = pygame.time.get_ticks()

        self.animate_movement(board, pawn, start_pos, end_pos, duration, start_time, clock)

        # Update fields of pawn and it's new square
        self.update_move(board, pawn, jump_square_number)

    @staticmethod
    def animate_movement(board, pawn, start_pos, end_pos, duration, start_time, clock):
        """
        Animate the movement of a pawn from start to end positions.

        Args:
            board (Board): The game board.
            pawn (Pawn): The pawn to be moved.
            start_pos (tuple): The starting position of the pawn.
            end_pos (tuple): The ending position of the pawn.
            duration (int): Duration of the movement in milliseconds.
            start_time (int): The starting time of the movement.
            clock (Clock): The Pygame clock for controlling animation.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            elapsed_time = pygame.time.get_ticks() - start_time
            elapsed_time = min(elapsed_time, duration)
            t = elapsed_time / duration

            current_pos = (
                start_pos[0] + int((end_pos[0] - start_pos[0]) * t),
                start_pos[1] + int((end_pos[1] - start_pos[1]) * t)
            )

            pawn.center = current_pos

            board.draw()
            pygame.display.flip()
            clock.tick(60)  # Limit the frame rate to 60 FPS

            if elapsed_time >= duration:
                break

    @staticmethod
    def delete_opponent_pawn(board, square_number):
        """
        Delete the opponent's pawn from the board.

        Args:
            board (Board): The game board.
            square_number (int): The square number occupied by the opponent's pawn.
        """
        opponent = board.get_occupying_pawn(square_number)
        if opponent:
            board.delete_pawn(opponent)

    @staticmethod
    def update_move(board, pawn, next_square_number):
        # Update fields of pawn and it's new square
        board.squares[pawn.square_number].free = True
        board.squares[next_square_number].free = False
        pawn.center = board.squares[next_square_number].get_center()
        pawn.square_number = next_square_number
        pawn.row, pawn.col = Square.compute_row_and_col(next_square_number)

        # Handle the case where the given move is a promoting move
        if pawn.is_promotion():
            board.promote_pawn(pawn)
            if board.is_original_board:
                board.draw()
                pygame.display.flip()

    @staticmethod
    def is_losing_team(board, pawn_team):
        if len(pawn_team) == 0:
            return True

        for pawn in pawn_team:
            next_squares = pawn.get_next_squares(board)
            next_jumping_squares = pawn.get_next_jumping_squares(board)
            if next_squares or next_jumping_squares:
                return False

        return True
