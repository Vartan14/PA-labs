from multi_way_merge import MultiWayMerge
import time


start_time = time.time()


print("256 = 1КB\n"
      "262144 = 1МB\n"
      "268435356 = 1ГB")

n = int(input("Enter amount of numbers: "))
n_files = int(input("Enter amount of files: "))


sorter = MultiWayMerge("Files/A.bin", "Files/D.bin", n, n_files)
sorter.sort()

print(f"\ntime: {(time.time() - start_time)}s seconds ")

