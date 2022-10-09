import os.path
import shutil
from random import randint

MAX_INT = 2147483647


class ReadFromFile:
    def __init__(self, path: str):
        self.path = path
        self.file = open(path, "rb")
        self.curr = self.file.read(4)
        self.next = self.file.read(4)

    def __next__(self):
        temp = self.curr
        self.curr = self.next
        self.next = self.file.read(4)
        return temp

    def close(self):
        self.file.close()


class MultiWayMerge:
    def __init__(self, path_a: str, path_d: str, n: int, n_files: int = 2):
        self.path_a = path_a
        self.path_d = path_d
        self.n = n
        self.n_files = n_files

    def create_file(self):
        with open(self.path_a, "wb") as a:
            for i in range(self.n):
                a.write(randint(1, MAX_INT).to_bytes(4, "big"))

    def sort(self):

        self.create_file()

        files_b_paths = []
        files_c_paths = []

        for i in range(self.n_files):
            files_b_paths.append(f"Files/B{i + 1}.bin")
            files_c_paths.append(f"Files/C{i + 1}.bin")

        # create C files
        for path in files_c_paths:
            with open(path, "wb") as file:
                pass

        self.first_distribution(files_b_paths)

        flag = True
        while not self.is_sorted(self.path_a, files_b_paths[0], files_c_paths[0]):
            if flag:
                self.merge(files_b_paths, files_c_paths)
            else:
                self.merge(files_c_paths, files_b_paths)
            flag = not flag

        if os.path.getsize(self.path_a) == os.path.getsize(files_b_paths[0]):
            shutil.copy(files_b_paths[0], self.path_d)
        else:
            shutil.copy(files_c_paths[0], self.path_d)

    @staticmethod
    def is_sorted(init_file: str, file_b1: str, file_c1: str) -> bool:
        return os.path.getsize(init_file) == os.path.getsize(file_b1) or \
               os.path.getsize(init_file) == os.path.getsize(file_c1)

    @staticmethod
    def are_all_empty(input_files: list) -> bool:
        for file in input_files:
            if file.curr:
                return False
        return True

    def first_distribution(self, files_b_paths: list):
        # open files
        a = ReadFromFile(self.path_a)
        files_B = []

        for path in files_b_paths:
            files_B.append(open(path, "wb"))

        # number of file
        j = 0

        # distribution
        while a.curr:
            files_B[j].write(a.curr)
            if a.curr > a.next:
                j = (j + 1) % self.n_files
            next(a)

        # close files
        a.close()
        for file in files_B:
            file.close()

    def merge(self, input_files_paths: list, output_files_paths: list):
        input_files = []
        output_files = []

        # open files
        for path in input_files_paths:
            input_files.append(ReadFromFile(path))

        for path in output_files_paths:
            output_files.append(open(path, "wb"))

        j = 0
        seq = []
        # main loop
        while not self.are_all_empty(input_files):
            min_val = MAX_INT
            min_ind = -1
            # find the smallest number among all input files
            for i in range(self.n_files):

                if input_files[i].curr:
                    num = int.from_bytes(input_files[i].curr, "big")

                    if not seq or num >= seq[-1]:

                        if num <= min_val:
                            min_val = num
                            min_ind = i

            # end of the sequence, writing the sequence in output file
            if min_ind < 0:
                for num in seq:
                    output_files[j].write(num.to_bytes(4, "big"))

                seq = []
                # change the file
                j = (j + 1) % self.n_files
            # continue of the sequence
            else:
                seq.append(min_val)
                next(input_files[min_ind])

        # writing the sequence in output file
        for num in seq:
            output_files[j].write(num.to_bytes(4, "big"))

        # close files
        for file in input_files:
            file.close()

        for file in output_files:
            file.close()


