class TicTacToe:
    def __init__(self,
                 first_player = 'X'):
        self.board = [None for _ in range(9)]
        self.current_player = first_player

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def plan_next_state(self, action):
        next_board = self.board[:]
        if next_board[action] is not None:
            raise Exception('Invalid action')
        next_board[action] = self.current_player

        return next_board, self.reward(next_board), int(not self.current_player)

    def play(self, action):
        if self.board[action] is not None:
            raise Exception('Invalid action')
        self.board[action] = self.current_player
        self.current_player = 'X' if self.current_player == 'O' else 'O'

        return self.reward()

    def reward(self,
               board = None):
        if board is None:
            board = self.board

        winner = self.get_winner(board)
        if winner == 'X':
            return (1, -1)
        elif winner == 'O':
            return (-1, 1)
        else:
            return (0, 0)

    def get_possible_actions(self):
        return [i for i, v in enumerate(self.board) if v is None]

    def get_winner(self,
                   board = None):
        if board is None:
            board = self.board

        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # vertical
            (0, 4, 8), (2, 4, 6)             # diagonal
        ]
        for a, b, c in winning_combinations:
            if board[a] == board[b] == board[c]:
                return board[a]
        return None
