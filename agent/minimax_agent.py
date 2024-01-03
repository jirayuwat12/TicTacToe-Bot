from agent import Agent

class MiniMaxAgent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def get_action(self, game):
        '''
        get the action of the agent
        :param game: game to get the action from
        :return: action
        '''
        action, score = self.minimax(game, depth=0)
        print(f'Action: {action}, Score: {score}')
        return action

    def minimax(self, game, board = None, depth = 0):
        '''
        minimax algorithm
        :param game: game to get the action from
        :param board: board to simulate on (default: game.board)
        :return: tuple (action, score)
        '''
        if board is None:
            board = game.board

        is_ended, winner = game.is_end(board)

        # if the game is ended
        if is_ended:
            return None, winner[0 if self.player == 'X' else 1]

        # if the game is not ended
        best_action = None
        best_score = -5 if depth%2==0 else 5
        for move in game.get_legal_moves(board):
            # simulate the move
            result = game.sim_move(move, board)
            action, score = self.minimax(game, result['final_board'], depth + 1)

            # if the game is ended
            if action is None:
                action = move

            if depth%2==0:
                if score > best_score:
                    best_score = score
                    best_action = action
            else:
                if score < best_score:
                    best_score = score
                    best_action = action

        game.print_board(board)
        return best_action, best_score
