import datetime
import os
from classes.pieces.king import King
from classes.pieces.pawn import Pawn

class MoveHandler:
    def __init__(self, board):
        self.board = board
        self.start_time = datetime.datetime.now()  # Game start time
        self.log_file = self.create_log_file()  # Creating a file to record moves

    def __del__(self):
        """
        Closing the file when the object is destroyed.
        """
        if hasattr(self, 'log_file'):
            self.log_file.close()

    def create_log_file(self):
        """
        Creates a file to record moves.
    :return: File object.
        """
        if not os.path.exists("data"):
            os.makedirs("data")
        filename = f"data/Game from {self.start_time.strftime('%Y-%m-%d %H-%M-%S')}.txt"
        return open(filename, "w", encoding="utf-8")

    def convert_to_chess_notation(self, position):
        """
        Converts coordinates from numeric format (row, column) to staggered format (column letter and row number).
        :param position: Tuple (row, column).
        :return: String in staggered notation (e.g. "a1").
        """
        row, col = position
        # Converting the column to a letter (0 -> 'a', 1 -> 'b', ..., 7 -> 'h')
        col_char = chr(ord('a') + col)
        # Convert the string to a number (0 -> 8, 1 -> 7, ..., 7 -> 1)
        row_num = 8 - row
        return f"{col_char}{row_num}"

    def log_move(self, move):
        """
        Writes a move to a file in chess notation.
        :param move: The move in the format ((start_row, start_col), (end_row, end_col)).
        """
        start_pos, end_pos = move
        start_chess = self.convert_to_chess_notation(start_pos)
        end_chess = self.convert_to_chess_notation(end_pos)
        move_str = f"{self.board.current_player} {start_chess} -> {end_chess}\n"
        self.log_file.write(move_str)
        self.log_file.flush()  # Flushing the buffer so that the data is immediately written to the file

    def handle_click(self, row, col):
        """
        Processes a click on a board cell.
        :param row: Cell row.
        :param col: Cell column.
        """
        if self.board.selected_piece is None:
            # If the chess piece is not selected, select the current players chess piece
            piece = self.board.grid[row][col]
            if piece is not None and piece.colour == self.board.current_player:
                self.board.selected_piece = piece
                self.board.valid_moves = piece.get_valid_moves(self.board.grid)

                # Filter valid moves if the king is in check
                if self.board.is_king_in_check(self.board.current_player):
                    self.board.valid_moves = self.filter_moves_in_check(self.board.selected_piece, self.board.valid_moves)
        else:
            # If the chess piece is already selected, check where the player clicked
            if (row, col) == self.board.selected_piece.position:
                # If you click on the same chess piece, cancel the selection
                self.board.selected_piece = None
                self.board.valid_moves = []
            elif (row, col) in self.board.valid_moves:
                # If you click on a valid move, execute it
                self.make_move(row, col)
            else:
                # If you click on another chess piece, select it (if it belongs to the current player)
                piece = self.board.grid[row][col]
                if piece is not None and piece.colour == self.board.current_player:
                    self.board.selected_piece = piece
                    self.board.valid_moves = piece.get_valid_moves(self.board.grid)

                    # Filter valid moves if the king is in check
                    if self.board.is_king_in_check(self.board.current_player):
                        self.board.valid_moves = self.filter_moves_in_check(self.board.selected_piece, self.board.valid_moves)

    def filter_moves_in_check(self, piece, valid_moves):
        """
        Filters valid moves to only those that remove the king from check.
    :param piece: The piece that moves.
    :param valid_moves: The list of valid moves.
    :return: The filtered list of valid moves.
        """
        filtered_moves = []

        for move in valid_moves:
            # Save the current state of the board
            temp_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
            temp_position = piece.position

            # Making a move
            self.board.grid[piece.position[0]][piece.position[1]] = None
            self.board.grid[move[0]][move[1]] = piece
            piece.position = move

            # Checking if the king is still in check
            if not self.board.is_king_in_check(self.board.current_player):
                filtered_moves.append(move)

            # Restore the board to its original state
            self.board.grid = [[temp_grid[row][col] for col in range(8)] for row in range(8)]
            piece.position = temp_position

        return filtered_moves

    def make_move(self, row, col):
        """
        Performs a move of a piece.
        :param row: Row of the cell.
        :param col: Column of the cell.
        """
        original_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
        original_position = self.board.selected_piece.position

        # Logging the move
        start_pos = self.board.selected_piece.position
        end_pos = (row, col)
        self.log_move((start_pos, end_pos))

        # Checking if the move is a castling move
        if isinstance(self.board.selected_piece, King) and abs(col - original_position[1]) == 2:
            self.handle_castle(row, col)
        else:
            # Normal move
            self.board.grid[self.board.selected_piece.position[0]][self.board.selected_piece.position[1]] = None
            self.board.grid[row][col] = self.board.selected_piece
            self.board.selected_piece.position = (row, col)

            # Checking if the king is still in check after the move
            if self.board.is_king_in_check(self.board.current_player):
                # If the king is in check, cancel the move
                self.board.grid = original_grid
                self.board.selected_piece.position = original_position
            else:
                # If the move is valid, complete it
                if self.board.grid[row][col] is not None and self.board.grid[row][col].colour != self.board.current_player:
                    self.board.grid[row][col] = None

                # Set the has_moved flag for the pawn
                if isinstance(self.board.selected_piece, Pawn):
                    self.board.selected_piece.has_moved = True

                # Changing the player
                self.board.current_player = "black" if self.board.current_player == "white" else "white"

        # Resetting the chess piece selection
        self.board.selected_piece = None
        self.board.valid_moves = []

    def handle_castle(self, row, col):
        """
        Performs a castling move.
        :param row: The king's row.
        :param col: The king's column after castling.
        """
        king = self.board.selected_piece
        king_row, king_col = king.position

        # Determining the direction of castling
        if col > king_col:  # Kingside castling
            rook_col = 7
            new_rook_col = col - 1
        else:  # Queenside castling
            rook_col = 0
            new_rook_col = col + 1

        # Moving the king
        self.board.grid[king_row][king_col] = None
        self.board.grid[row][col] = king
        king.position = (row, col)
        king.has_moved = True

        # Moving the rook
        rook = self.board.grid[king_row][rook_col]
        self.board.grid[king_row][rook_col] = None
        self.board.grid[king_row][new_rook_col] = rook
        rook.position = (king_row, new_rook_col)
        rook.has_moved = True

        # Changing the player
        self.board.current_player = "black" if self.board.current_player == "white" else "white"
