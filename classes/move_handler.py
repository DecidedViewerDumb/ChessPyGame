from classes.pieces.pawn import Pawn


class MoveHandler:
    def __init__(self, board):
        self.board = board

    def handle_click(self, row, col):
        """
        Обрабатывает клик на клетку доски.
        :param row: Строка клетки.
        :param col: Столбец клетки.
        """
        if self.board.selected_piece is None:
            piece = self.board.grid[row][col]
            if piece is not None and piece.color == self.board.current_player:
                self.board.selected_piece = piece
                self.board.valid_moves = piece.get_valid_moves(self.board.grid)

                if self.board.is_king_in_check(self.board.current_player):
                    self.board.valid_moves = self.filter_moves_in_check(self.board.selected_piece, self.board.valid_moves)
        else:
            if (row, col) in self.board.valid_moves:
                original_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
                original_position = self.board.selected_piece.position

                self.board.grid[self.board.selected_piece.position[0]][self.board.selected_piece.position[1]] = None
                self.board.grid[row][col] = self.board.selected_piece
                self.board.selected_piece.position = (row, col)

                if self.board.is_king_in_check(self.board.current_player):
                    self.board.grid = original_grid
                    self.board.selected_piece.position = original_position
                else:
                    if self.board.grid[row][col] is not None and self.board.grid[row][col].color != self.board.current_player:
                        self.board.grid[row][col] = None

                    if isinstance(self.board.selected_piece, Pawn):
                        self.board.selected_piece.has_moved = True

                    self.board.current_player = "black" if self.board.current_player == "white" else "white"

            self.board.selected_piece = None
            self.board.valid_moves = []

    def filter_moves_in_check(self, piece, valid_moves):
        """
        Фильтрует допустимые ходы, оставляя только те, которые убирают короля из-под шаха.
        :param piece: Фигура, которая ходит.
        :param valid_moves: Список допустимых ходов.
        :return: Отфильтрованный список допустимых ходов.
        """
        filtered_moves = []

        for move in valid_moves:
            temp_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
            temp_position = piece.position

            self.board.grid[piece.position[0]][piece.position[1]] = None
            self.board.grid[move[0]][move[1]] = piece
            piece.position = move

            if not self.board.is_king_in_check(self.board.current_player):
                filtered_moves.append(move)

            self.board.grid = [[temp_grid[row][col] for col in range(8)] for row in range(8)]
            piece.position = temp_position

        return filtered_moves
