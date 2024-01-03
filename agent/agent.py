class Agent:
    def __init__(self,
                 player):
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
        raise NotImplementedError()
