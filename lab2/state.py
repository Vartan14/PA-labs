from copy import copy


class State:
    def __init__(self, queens, depth=0):
        self._queens = copy(queens)
        self._depth = copy(depth)

    def is_solution(self):
        for i in range(len(self._queens) - 1):
            for j in range(i + 1, len(self._queens)):
                dist = j - i  # distance between columns
                # same diagonal
                if self._queens[i] == self._queens[j] or self._queens[i] - dist == self._queens[j] or \
                        self._queens[i] + dist == self._queens[j]:
                    return False
        return True

    def move(self, row, col):
        self._queens[row] = col

    def get_depth(self):
        return self._depth

    def set_depth(self, depth):
        self._depth = depth

    def get_queens(self):
        return self._queens

    def __f1_heuristic(self):
        num_of_pairs = 0

        for i in range(len(self._queens) - 1):
            is_visible_row = True   # visibility in row
            is_visible_d1 = True    # visibility in left diagonal
            is_visible_d2 = True    # visibility in left diagonal

            for j in range(i + 1, len(self._queens)):
                dist = j - i
                if self._queens[i] == self._queens[j] and is_visible_row:
                    num_of_pairs += 1
                    is_visible_row = False
                if self._queens[i] == self._queens[j] - dist and is_visible_d1:
                    num_of_pairs += 1
                    is_visible_d1 = False
                if self._queens[i] == self._queens[j] + dist and is_visible_d2:
                    num_of_pairs += 1
                    is_visible_d2 = False
        return num_of_pairs

    def __priority(self):
        return self.__f1_heuristic() + self._depth

    def __gt__(self, other):
        return self.__priority() > other.__priority()
