import numpy as np



def example_function():
    rand_one = np.array([np.random.randint(1, i+5) for i in range(10)])
    rand_two = np.random.normal(3, 13)

    total = rand_one * rand_two
    rand_three = np.random.normal(3, 19) + np.random.normal(1, 5) + np.random.standard_cauchy()

    return total + rand_three


[example_function() for _ in range(5)]


def test_function():
    return "Hello"


running = np.random.poisson(1)
while running < 10:
    running += 1 
    test_function()
