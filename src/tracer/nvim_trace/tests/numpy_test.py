import numpy as np
import time
import sys


from nvim_trace.__main__ import Tracer
tracer = Tracer()
sys.setprofile(tracer.__call__)
sys.settrace(tracer.__call__)
time.sleep(0.1)

import test_files.other_test
import test_files.numpy_test

sys.settrace(None)
sys.setprofile(None)
