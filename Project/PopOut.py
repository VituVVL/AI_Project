class PopOutGame:
    ROWS = 6
    COLS = 7
    EMPTY = '-'

    def __init__(self):
        self.board = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 'X'

    def clone(self):
        """Cria uma cópia do estado do jogo (útil para algoritmos de pesquisa depois)."""
        new_game = PopOutGame()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        return new_game

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def print_board(self):
        print()
        for row in self.board:
            print(''.join(row))
        print()
        #print(" 1234567")
        print()

    def is_column_full(self, col):
        return self.board[0][col] != self.EMPTY

    def is_valid_drop(self, col):
        return 0 <= col < self.COLS and not self.is_column_full(col)

    def is_valid_pop(self, col):
        return 0 <= col < self.COLS and self.board[self.ROWS - 1][col] == self.current_player

    def drop_piece(self, col):
        """Coloca a peça do jogador atual na posição mais baixa disponível da coluna."""
        if not self.is_valid_drop(col):
            return False

        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == self.EMPTY:
                self.board[row][col] = self.current_player
                return True
        return False

    def pop_piece(self, col):
        """
        Remove a peça de baixo da coluna, se ela pertencer ao jogador atual,
        e empurra as peças acima para baixo.
        """
        if not self.is_valid_pop(col):
            return False

        for row in range(self.ROWS - 1, 0, -1):
            self.board[row][col] = self.board[row - 1][col]
        self.board[0][col] = self.EMPTY
        return True

    def apply_move(self, move_type, col):
        """
        Aplica uma jogada.
        move_type: 'drop' ou 'pop'
        col: índice da coluna (0 a 6)
        """
        if move_type == 'drop':
            return self.drop_piece(col)
        elif move_type == 'pop':
            return self.pop_piece(col)
        return False

    def get_legal_moves(self):
        """
        Retorna lista de jogadas possíveis no formato:
        [('drop', col), ('pop', col), ...]
        Isso será muito útil para IA depois.
        """
        moves = []

        for col in range(self.COLS):
            if self.is_valid_drop(col):
                moves.append(('drop', col))
            if self.is_valid_pop(col):
                moves.append(('pop', col))

        return moves

    def board_full(self):
        return all(self.board[0][col] != self.EMPTY for col in range(self.COLS))

    def check_winner_for(self, player):
        """Verifica se o jogador informado tem 4 em linha."""
        # Horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Diagonal principal (\)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Diagonal secundária (/)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def get_game_result(self):
        """
        Retorna:
        'X' se X venceu
        'O' se O venceu
        'DRAW' se empate
        None se o jogo continua

        Observação:
        após um pop, pode acontecer de ambos criarem 4 em linha.
        Aqui tratei isso como empate.
        """
        x_wins = self.check_winner_for('X')
        o_wins = self.check_winner_for('O')

        if x_wins and o_wins:
            return 'DRAW'
        elif x_wins:
            return 'X'
        elif o_wins:
            return 'O'
        elif self.board_full() and len(self.get_legal_moves()) == 0:
            return 'DRAW'
        else:
            return None

    def print_instructions(self):
        print("Game Interface")
        print("The board uses 6 rows and 7 columns.")
        print("Players: X and O")
        print("Move types:")
        print("  drop -> place a piece in a column")
        print("  pop  -> remove your bottom piece from a column")
        print()
        print("Examples:")
        print("  drop 4")
        print("  pop 2")
        print()

    def play(self):
        self.print_instructions()

        while True:
            self.print_board()

            result = self.get_game_result()
            if result == 'X':
                print("X wins!")
                break
            elif result == 'O':
                print("O wins!")
                break
            elif result == 'DRAW':
                print("It's a draw!")
                break

            print(f"It is now {self.current_player}'s turn.")
            #print("Make a move by choosing the type of move (drop or pop) and the column.")
            #print("Example: drop 4")
            move_input = input("> ").strip().lower()

            parts = move_input.split()

            if len(parts) != 2:
                print("Invalid format. Use: drop 4  or  pop 2")
                continue

            move_type, col_str = parts

            if move_type not in ('drop', 'pop'):
                print("Invalid move type. Use 'drop' or 'pop'.")
                continue

            if not col_str.isdigit():
                print("Column must be a number from 1 to 7.")
                continue

            col = int(col_str) - 1

            if not (0 <= col < self.COLS):
                print("Column must be between 1 and 7.")
                continue

            success = self.apply_move(move_type, col)

            if not success:
                if move_type == 'drop':
                    print("Invalid drop. That column is full.")
                else:
                    print("Invalid pop. You can only pop your own bottom piece.")
                continue

            self.switch_player()


if __name__ == "__main__":
    game = PopOutGame()
    game.play()