from game.tictactoe import TicTacToe

env = TicTacToe()

def print_board(board):
    print('-------------')
    for i in range(3):
        print('|', end = '')
        for j in range(3):
            print(' {} |'.format(board[i * 3 + j] if board[i * 3 + j] is not None else str(i*3+j)), end = '')
        print('\n-------------')

print('Welcome to Tic-Tac-Toe!')
print(f'You are playing as {env.get_current_player()}')

while True:
    print_board(env.get_board())

    reward = env.reward()
    if reward[0] != 0:
        print(f"Game over! Winner: {'X' if reward[0] == 1 else 'O'}")
        break

    print(f"Current player: {env.get_current_player()}")
    print(f'Possible actions: {env.get_possible_actions()}')
    action = int(input('Enter your action: '))

    try:
        env.play(action)
    except Exception as e:
        print(e)
        continue
