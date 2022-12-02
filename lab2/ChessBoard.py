import random
from queue import Queue, PriorityQueue
from termcolor import colored
from time import time
from state import State


class ChessBoard:
    def __init__(self, n):
        self.__n = n

    def input_queens(self):
        try:
            while True:
                s = input(f"Enter {self.__n} queens in format '1 1 1 1 1 1 1 1': ")
                condition = True
                queens = list(map(int, s.split()))
                for num in queens:
                    if int(num) >= self.__n:
                        condition = False

                if len(s.replace(' ', '')) == self.__n and condition:
                    break
            queens = list(map(int, s.split()))
            state = State(queens)
            return state

        except ValueError:
            print('Wrong input')
            exit()

    def generate_queens(self):
        queens = [random.randint(0, self.__n - 1) for x in range(self.__n)]
        state = State(queens, 0)
        return state

    def print_state(self, state: State):
        nums = ''.join(str(x) + ' ' * 5 if x < 9 else str(x) + ' ' * 4 for x in range(self.__n))
        print(colored('\n       ' + nums, 'red'), end='')
        print(colored('\n    -' + '------' * self.__n, 'blue'))
        queens = state.get_queens()
        for i in range(self.__n):
            text = f'{i}   ' if i < 10 else f'{i}  '
            print(colored(text, 'red'), end='')
            print(colored('|  ', 'blue'), end='')
            for j in range(self.__n):
                if queens[j] == i:
                    print(colored('Q', 'green'), end='')
                    print(colored('  |  ', 'blue'), end='')
                else:
                    print(colored('   |  ', 'blue'), end='')
            print(colored('\n    -' + '------' * self.__n, 'blue'))

        print(f"Queens: {queens}")

    def BFS_solution(self, initial_state):
        start_time = time()
        q = Queue()
        q.put(initial_state)

        iterations = 0
        total_states = 1
        states_in_mem = 1

        while not q.empty():

            if time() - start_time >= 1800:
                print('Time limit!')
                return False

            iterations += 1
            curr_state = q.get()
            states_in_mem -= 1

            if curr_state.is_solution():
                return curr_state, iterations, total_states, states_in_mem, time() - start_time

            curr_depth = curr_state.get_depth()
            if curr_depth != self.__n:
                for i in range(self.__n):
                    new_state = State(curr_state.get_queens(), curr_depth + 1)
                    new_state.move(curr_depth, i)  # queens[row] = col
                    q.put(new_state)
                    total_states += 1
                    states_in_mem += 1

    def A_star_solution(self, initial_state):
        start_time = time()
        q = PriorityQueue()
        q.put(initial_state)

        iterations = 0
        total_states = 1
        states_in_mem = 1

        while not q.empty():

            if time() - start_time >= 1800:
                return False

            iterations += 1
            curr_state = q.get()
            states_in_mem -= 1

            if curr_state.is_solution():
                return curr_state, iterations, total_states, states_in_mem, time() - start_time

            curr_depth = curr_state.get_depth()
            if curr_depth != self.__n:
                for i in range(self.__n):
                    new_state = State(curr_state.get_queens(), curr_depth + 1)
                    new_state.move(curr_depth, i)  # queens[row] = col
                    q.put(new_state)
                    total_states += 1
                    states_in_mem += 1


if __name__ == '__main__':
    my_board = ChessBoard(8)
    #init_state = my_board.input_queens()
    init_state = my_board.generate_queens()
    print('\nInitial state:')
    my_board.print_state(init_state)

    bfs_solution = my_board.BFS_solution(init_state)
    print("\nBFS solution:")

    my_board.print_state(bfs_solution[0])
    print(f'iterations: {bfs_solution[1]}\n'
          f'total states: {bfs_solution[2]}\n'
          f'states in memory: {bfs_solution[3]}\n'
          f'time: {bfs_solution[4]}')

    solution = my_board.A_star_solution(init_state)
    print("\nA star solution:")
    my_board.print_state(solution[0])
    print(f'iterations: {solution[1]}\n'
          f'total states: {solution[2]}\n'
          f'states in memory: {solution[3]}\n'
          f'time: {solution[4]}')
