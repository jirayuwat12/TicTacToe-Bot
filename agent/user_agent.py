from agent import Agent

class UserAgent(Agent):
    def __init__(self, player):
        '''
        :param player: player of the agent
        '''
        self.player = player

    def get_action(self, game):
        '''
        get an action
        :param game: game to get action from
        :return: action
        '''
        print(f"Possible mode is : {game.get_legal_moves()}")
        move = int(input("Enter a move: "))
        return move
