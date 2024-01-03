import random
from agent import Agent

class RandomAgent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def get_action(self, game):
        return random.choice(game.get_legal_moves())
