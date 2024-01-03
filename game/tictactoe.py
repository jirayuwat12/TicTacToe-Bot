import random


class TicTacToe:
    def __init__(self):
        self.board = [None for _ in range(9)]
        self.current_player = random.randint(0, 1)

    def move(self, moves):
        '''
        make a move
        :param moves: move to make
        :return: no return value (the board is updated)
        '''
        if not isinstance(moves, list):
            moves = [moves]
        
        for move in moves:
            if self.board[move] is not None:
                raise Exception('Illegal move')
            self.board[move] = 'X' if self.current_player == 0 else 'O'
            self.current_player = 1 - self.current_player

            if self.is_end()[0]:
                return

    def sim_move(self, moves, board = None):
        '''
        simulate a move
        :param moves: move to simulate
        :param board: board to simulate on (default: self.board)
        :return: dictionary of the form {'winner': winner, 'final_board': board, 'is_ended': is_ended, 'legal_moves': legal_moves}
        '''
        if not isinstance(moves, list):
            moves = [moves]
        
        if board is None:
            board = self.board
        board = board.copy()

        for move in moves:
            if board[move] is not None:
                raise Exception(f'Illegal move({move} {self.current_player} {board} {self.get_legal_moves(board)})')
            board[move] = 'X' if self.current_player == 0 else 'O'
            self.current_player = 1 - self.current_player
            if self.is_end(board)[0]:
                return {
                    'winner': self.get_winner(board),
                    'final_board': board,
                    'is_ended': True,
                    'legal_moves': []
                }
        return {
            'winner': None,
            'final_board': board,
            'is_ended': False,
            'legal_moves': self.get_legal_moves(board)
        }

    def is_end(self, board = None):
        '''
        check if the game is ended
        :param board: board to check (default: self.board)
        :return: tuple (is_ended, winner)
        '''
        if board is None:
            board = self.board

        winner = self.get_winner(board)
        if winner is not None:
            return True, winner
        return False, None

    def get_winner(self, board = None):
        '''
        get the winner of the board
        :param board: board to check (default: self.board)
        :return: tuple of 2 elements the score of player 1 and the score of player 2 respectively (if the game is ended else None)
        '''
        if board is None:
            board = self.board
    
        possible_wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # vertical
            (0, 4, 8), (2, 4, 6) # diagonal
        ]
        for pos in possible_wins:
            if board[pos[0]] is not None and board[pos[0]] == board[pos[1]] == board[pos[2]]:
                return (
                    1 if board[pos[0]] == 'X' else -1,
                    1 if board[pos[0]] == 'O' else -1,
                )
        if None not in board:
            return (0, 0)
        return None

    def get_legal_moves(self, board = None):
        '''
        get the legal moves of the board
        :param board: board to check (default: self.board)
        :return: list of legal moves
        '''
        if board is None:
            board = self.board

        return [i for i in range(9) if board[i] is None]

    def reset(self):
        '''
        reset the board
        :return: no return value (the board is updated)
        '''
        self.board = [None for _ in range(9)]
        self.current_player = random.randint(0, 1)

    def print_board(self, board = None):
        '''
        print the board
        :param board: board to print(default: self.board)
        '''
        if board is None:
            board = self.board

        print('----------')
        for i in range(3):
            print('|', end='')
            for j in range(3):
                print(' ' if board[i * 3 + j] is None else board[i * 3 + j], end=' |')
            print()
            print('----------')
        print()

    def get_board_id(self, board = None):
        '''
        hash the board to an integer
        :param board: board to hash (default: self.board)
        :return: hash value
        '''
        if board is None:
            board = self.board

        id = 0
        for i in range(9):
            id += (3 ** i) * (0 if board[i] is None else (1 if board[i] == 'X' else 2))

        return id
