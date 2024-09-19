import numpy as np


for i in range(10):
    x = 0
    y = np.exp(3 * np.random.standard_cauchy())
    z = np.exp(3 * np.random.standard_cauchy() / np.random.standard_cauchy() * np.random.normal())
    v = np.array([[x + y + z]*10000]).dot(np.random.normal(10000))
    v = 0
    v = 0
    
    x = np.random.standard_cauchy()
    x = np.random.standard_cauchy(size=(100,1))
    y = np.random.random_integers(0, 1000, size=(100,1))
    z = np.sin(x + y) + np.random.uniform(0, x) / np.exp(x)
