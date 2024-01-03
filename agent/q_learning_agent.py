import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

from agent import Agent

class QLearningAgent(Agent):
    def __init__(self,
                 player='X',
                 gamma=0.95,
                 learning_rate=5e-2,
                 n_action=9,
                 n_state=3**9,
                 max_epsilon=0.8,
                 min_epsilon=0.01,
                 q_table=None):
        super().__init__(player)  # Call the base class __init__ method
        self.player = player

        self.gamma = gamma
        self.learning_rate = learning_rate
        self.epsilon = max_epsilon
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.n_train = 0

        self.n_action = n_action
        self.n_state = n_state
        if q_table is not None:
            self.load_q_table(q_table)
            if self.q_table.shape != (n_state, n_action):
                raise Exception('q_table shape does not match')
        else:
            self.q_table = np.random.uniform(low=-1e-3, high=1e-3, size=(n_state, n_action))


    def train(self,
              n_game = 100,
              enemy = None,
              environment = None):
        '''
        train the agent by self-play
        :param n_game: number of games to play during training
        :param enemy: the opponent agent (default: self)

        :return: no return value
        '''
        if enemy is None:
            enemy = QLearningAgent(player='X' if self.player == 'O' else 'O',
                                    gamma=self.gamma,
                                    learning_rate=self.learning_rate,
                                    n_action=self.n_action,
                                    n_state=self.n_state,
                                    max_epsilon=self.max_epsilon,
                                    min_epsilon=self.min_epsilon)
        if environment is None:
            raise Exception('environment is not provided')

        # get plt ready
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Q Table')
        plt.show()

        total_win = 0
        first_player = None

        looper = tqdm(range(n_game), desc=f'Training {self.player}')
        for _ in looper:
            # reset game
            environment.reset()
            first_player = environment.current_player

            while True:
                # let's enemy play
                if environment.current_player == enemy.player:
                    action = enemy.get_action(environment)
                    if action not in environment.get_legal_moves():
                        action = np.random.choice(environment.get_legal_moves())
                    environment.move(action)
                    continue

                # calculate epsilon from max and min epsilon
                self.epsilon = self.min_epsilon + (n_game - _  + 1) * (self.max_epsilon - self.min_epsilon) / n_game

                # get action
                if np.random.uniform() < self.epsilon:
                    action = np.random.choice(environment.get_legal_moves())
                else:
                    action = self.get_action(environment)
                    if action not in environment.get_legal_moves():
                        action = np.random.choice(environment.get_legal_moves())

                # simulate action
                result = environment.sim_move(action)
                environment.move(action)
                winner = result['winner']
                final_board = result['final_board']
                is_ended = result['is_ended']
                legal_moves = result['legal_moves']

                # update q table for both players
                current_state = environment.get_board_id()
                next_state = environment.get_board_id(final_board)
                current_reward = 0 if winner is None else winner[self.player == 'O']
                max_next_q_value = np.max(self.q_table[next_state, :])
                q_value = self.q_table[current_state, action]

                new_q = q_value + self.learning_rate * (current_reward + self.gamma * max_next_q_value - q_value)
                self.q_table[current_state, action] = new_q

                # update stat
                if winner is not None and winner[self.player == 'O'] == 1:
                    total_win += 1

                looper.set_postfix({
                    'winner': 'None' if winner is None else 'O' if winner[1]==1 else 'X',
                    'first_player': 'O' if first_player == 1 else 'X',
                    'diff': new_q - q_value,
                    'epsilon': self.epsilon,
                    'win_rate' : total_win / (_ + 1)
                })

                # check if game is ended
                if is_ended:
                    break

            # visualize q table with matplotlib
            if _ % 50 == 0:
                ax.clear()
                ax.set_title('Q Table')
                img = np.array(self.q_table).reshape((3**5, 3**5, 3))
                img = (img - np.min(img)) / (np.max(img) - np.min(img))
                ax.imshow(img)
                plt.pause(0.001)
        
        plt.close()


    def get_action(self, environment):
        '''
        get an action given the current state
        :param environment: current state
        
        :return: action
        '''
        action = np.argmax(self.q_table[environment.get_board_id(), :])
        if action not in environment.get_legal_moves():
            action = np.random.choice(environment.get_legal_moves())
        return action

    def save_q_table(self, path):
        np.save(path, self.q_table)

    def load_q_table(self, path):
        self.q_table = np.load(path)
        print(f'Loaded q_table from {path}')
        print(self.q_table.shape)

    def update_epsilon(self):
        self.epsilon = self.min_epsilon + (30000 - min(self.n_train,30000) + 1) * (self.max_epsilon - self.min_epsilon) / 30000
        self.n_train += 1