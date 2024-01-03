import sys

sys.path.append('./agent')
from user_agent import UserAgent
from random_agent import RandomAgent
from minimax_agent import MiniMaxAgent
from q_learning_agent import QLearningAgent
sys.path.append('./game')
from game.tictactoe import TicTacToe

game = TicTacToe()

agent_x = UserAgent('X')
agent_o = QLearningAgent('O', q_table='q_table_o.npy')

while True:
    # print the board
    print('Current board:')
    game.print_board()

    # get the action from the agent
    print(f'Player {"X" if game.current_player == 0 else "O"}\'s turn')
    if game.current_player == 0:
        action = agent_x.get_action(game)
    else:
        action = agent_o.get_action(game)

    # make the move
    game.move(action)

    # check if the game is ended
    ended, winner = game.is_end()
    if ended:
        print('Final board:')
        game.print_board()

        if winner == (0, 0):
            print('Game ended in a draw')
        else:
            print(f'Game ended, winner is {"X" if winner[0] == 1 else "O"}')
        break
