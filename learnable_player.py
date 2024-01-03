import sys
sys.path.append('./game')
sys.path.append('./agent')

from tictactoe import TicTacToe
from q_learning_agent import QLearningAgent

if __name__ == "__main__":
    learnable_agent_x = QLearningAgent(player='X', q_table='q_table_x.npy')
    learnable_agent_o = QLearningAgent(player='O', q_table='q_table_o.npy')

    game = TicTacToe()

    for _ in range(30):
        learnable_agent_x.train(n_game=1000, environment=game, enemy=learnable_agent_o)
        learnable_agent_o.train(n_game=1000, environment=game, enemy=learnable_agent_x)

        learnable_agent_x.save_q_table('q_table_x.npy')
        learnable_agent_o.save_q_table('q_table_o.npy')

    print('Average for each action:')
    print('X:')
    print(learnable_agent_x.q_table.mean(axis=0))
    print('O:')
    print(learnable_agent_o.q_table.mean(axis=0))

