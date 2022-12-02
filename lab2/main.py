import sys
from ChessBoard import ChessBoard

queens_input = 0
algo = 0
size = 0

while size > 20 or size < 4:
    try:
        size = int(input('Enter board size (min: 4, max: 20): '))
    except ValueError:
        sys.exit('Type number!')

while queens_input != '1' and queens_input != '2':
    queens_input = input('Do you want to input or generate queens:\n1 - input\n2 - generate\n')

while algo != '1' and algo != '2':
    algo = input('Choose the algorithm:\n1 - BFS\n2 - A star\n')

# create board
my_board = ChessBoard(size)

# create initial state
if queens_input == '1':
    init_state = my_board.input_queens()
else:
    init_state = my_board.generate_queens()

# print initial state
print('\nInitial state:')
my_board.print_state(init_state)

# solution
if algo == '1':
    solution = my_board.BFS_solution(init_state)
    print("\nBFS solution:")
else:
    solution = my_board.A_star_solution(init_state)
    print("\nA star solution:")

# print solution
if solution:
    my_board.print_state(solution[0])
    print(f'iterations: {solution[1]}\n'
          f'total states: {solution[2]}\n'
          f'states in memory: {solution[3]}\n'
          f'time: {solution[4]}')
