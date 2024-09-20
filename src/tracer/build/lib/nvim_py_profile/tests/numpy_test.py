

import numpy as np


print("Hello")

values = np.random.random_integers(1, 10)
large_array = np.random.normal(5, 10, size=(1000000, 1))
values = values ** 5 
sec_large = np.random.exponential(10, size=(10000, 1000))
v = large_array + sec_large
could_take_a_while = np.random.exponential(10, size=(1000, 1000))
could_take_a_while += np.random.exponential(10, size=(1000, 1000))

