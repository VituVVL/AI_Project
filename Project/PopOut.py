import MCTS 
import csv
import os
import time

class PopOutGame:
    ROWS = 6
    COLS = 7
    EMPTY = '-'
    #Verificar se o git funcionou!!

    #Cria o tabuleiro vazio
    def __init__(self):
        self.board = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 'X'

        self.last_player = None
        self.last_move_type = None

        #Variavel que nos permite cumprir se um estado se repetir 3 vezes, é empate
        self.state_history = {}
        self._record_state() #Grava estado inicial do tabuleiro
    
    #Função para guardar os estados do tabuleiro
    def _record_state(self):
        state_tuple = tuple(tuple(row) for row in self.board)
        self.state_history[state_tuple] = self.state_history.get(state_tuple, 0) + 1

    #Função que cria uma copia do tabuleiro para se puder usar para os testes da IA
    def clone(self):
        """Cria uma cópia do estado do jogo (útil para algoritmos de pesquisa depois)."""
        new_game = PopOutGame()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player

        #Copiar os novos atributos
        new_game.last_player = self.last_player
        new_game.last_move_type = self.last_move_type
        new_game.state_history = self.state_history.copy()

        return new_game

    #Função de troca de jogadores
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    #Função para imprimir o tabuleiro
    def print_board(self):
        print()
        for row in self.board:
            print(''.join(row))
        print()

    #Verifica se coluna esta cheia
    def is_column_full(self, col):
        return self.board[0][col] != self.EMPTY

    #Verificar se o drop esta dentro dos parametros
    def is_valid_drop(self, col):
        return 0 <= col < self.COLS and not self.is_column_full(col)

    #Verificar se o pop esta dentro dos parametros
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
        """Aplica uma jogada (drop ou pop) e regista o histórico."""
        success = False
        if move_type == 'drop':
            success = self.drop_piece(col)
        elif move_type == 'pop':
            success = self.pop_piece(col)
        
        if success:
            self.last_player = self.current_player
            self.last_move_type = move_type
            self._record_state()

        return success

    def get_legal_moves(self):
        """
        Retorna lista de jogadas possíveis no formato:
        [('drop', col), ('pop', col), ...]
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
        """Verifica o estado do jogo e aplica as regras do PopOut."""
        x_wins = self.check_winner_for('X')
        o_wins = self.check_winner_for('O')

        # Se um pop cria 4 em linha para ambos, o jogador que fez o pop ganha e o outro é ignorado.
        if x_wins and o_wins:
            if self.last_move_type == 'pop':
                return self.last_player
            else:
                return 'DRAW'
            
        elif x_wins:
            return 'X'
        elif o_wins:
            return 'O'
        
        # Se o mesmo estado se repete 3 vezes, o jogo é declarado empate.
        current_state = tuple(tuple(row) for row in self.board)
        if self.state_history.get(current_state, 0) >= 3:
            return 'DRAW'

        #Verifica se não há mais movimentos possíveis (empate por bloqueio)
        if self.board_full() and len(self.get_legal_moves()) == 0:
            return 'DRAW'
        

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

    def print_menu_inicial(self):
        
        print("PopOut")
        print("1- USER vs USER")
        print("2- USER vs IA") #USER vs IA(MonteCarlo)
        while(True):
            op = input("> ").strip()
            if(op=="1" or op=="2"):
                return op

    def generate_dataset(self, num_games=50, iterations=3000):

        """Cronómetro temporario para teste de tempos de execução após mudanças"""
        tempo_inicio = time.time()

        """
        Duas IAs a jogar uma contra a outra e guarda as 
        decisões num ficheiro CSV
        """
        print(f"A iniciar a geração de {num_games} jogos (iterações: {iterations})")
        
        filename = f"dataset_popout_{iterations}.csv"

        ficheiro_existe = os.path.isfile(filename)

        # 1. Abrir o ficheiro CSV em modo de escrita ('w')
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Só escrevemos o cabeçalho (a primeira linha do Excel/CSV) se o ficheiro acabou de ser criado
            if not ficheiro_existe:
                writer.writerow(['Board_State', 'Best_Move'])

            # 2. O Ciclo dos Jogos
            for i in range(num_games):
                print(f"A simular jogo {i + 1} de {num_games}...")
                
                # Cria um tabuleiro novo e limpo para esta partida
                sim_game = PopOutGame()
                
                # Cria os dois "cérebros" com as tuas 3000 iterações
                ia_X = MCTS.MCTS(ai_player='X', iterations=iterations)
                ia_O = MCTS.MCTS(ai_player='O', iterations=iterations)

                # 3. O Ciclo de Turnos (jogar até o jogo acabar)
                while sim_game.get_game_result() is None:
                    

                    if(sim_game.current_player == 'X'):
                        best_move = ia_X.search(sim_game) 
                    else:
                        best_move = ia_O.search(sim_game)
                    
                    
                    estado_tabuleiro = str(sim_game.board)
                    jogada = f"{best_move[0]} {best_move[1]}"
                    
                    writer.writerow([estado_tabuleiro, jogada])
                    
                    # Aplicar a jogada no tabuleiro
                    sim_game.apply_move(best_move[0], best_move[1])

                    # Avisar as duas ia's que a jogada aconteceu
                    # Assim avançam a árvore e não começam do zero
                    ia_X.update_root(best_move)
                    ia_O.update_root(best_move)
                    #ia_X.root = None
                    #ia_O.root = None
                    
                    # Trocar de jogador para o próximo turno.
                    sim_game.switch_player()

        tempo_fim = time.time()
        tempo_total = tempo_fim - tempo_inicio

        print(f"\n✅ Geração concluída! Ficheiro '{filename}' criado com sucesso.")
        print(f"Tempo Total de execução {tempo_total:.2f}")

        """
        Versao que nao aproveita árvore e cria sempre uma nova : 16.49 segundos
        Versao que utiliza árvore ja criada : 
        """

    def play(self):
        modo_jogo = self.print_menu_inicial()

        self.print_instructions()

        ia = MCTS.MCTS(ai_player = "O", iterations = 3000)

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

            print(f"It is now {self.current_player}'s turn. Enter move (drop/pop + column): ")

            # Regra do tabuleiro cheio
            if self.board_full():
                print("O tabuleiro está cheio! Podes fazer um 'pop' ou declarar empate.")
                draw_choice = input("Queres terminar com empate? (sim/nao): ").strip().lower()
                if draw_choice in ['sim', 's']:
                    print("O jogo terminou em empate por decisão do jogador!")
                    break

            # Loop interno para insistir até o jogador fazer uma jogada válida
            while True:
                #Se for o X é o Humano
                if((self.current_player == "X" and modo_jogo == "2") or (modo_jogo == "1")):
                    move_input = input(f"{self.current_player}> ").strip().lower()
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

                    # Sai do loop interno quando a jogada é válida
                    break
                else:
                    jogada_ia = ia.search(self)
                    print(f"A IA jogou {jogada_ia[0]} na coluna {jogada_ia[1]+1}")
                    self.apply_move(jogada_ia[0], jogada_ia[1])
                    #jogada_ia[0] = 'drop' ou 'pop'
                    #jogada_ia[1] = nr da coluna
                    break

            self.switch_player()


if __name__ == "__main__":
    game = PopOutGame()
    #game.play() #Temporário
    game.generate_dataset(num_games=1)