import os
import sys
try:
    os.chdir("driver")
    sys.path.insert(0, "driver")
    from running import run
except FileNotFoundError:
    print("не удалось найти библиотеки")    