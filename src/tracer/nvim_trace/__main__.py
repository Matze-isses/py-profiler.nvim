import logging
import profile, pstats, io
import profile
import numpy as np
import time
import sys
import linecache

from nvim_trace.sender import Sender
from nvim_trace.utils.logging import PackageLogger
from nvim_trace.utils.process_frames import Processor
from nvim_trace.utils.line_data import FData


class Tracer:

    def __init__(self):

        self._logger = PackageLogger()
        self._logger.addHandler(logging.StreamHandler())
        self._processor = Processor(self._logger)
        self._send = Sender()
        self._recursion_level = 0
        self._max = 3
        self._times = [("", 0)]

        self.pending_lines = []
        self._context = {}
        self._call_counting = {}
        self.always_in_vars = {}
        self._vars_before = {}
        self.profile = profile.Profile(timer=time.perf_counter_ns)
        self.data = []

    def __call__(self, frame, event, args):
        in_current_file = frame.f_code.co_filename.startswith("/home/admin/nvim/")

        filename = frame.f_code.co_filename
        line_code = frame.f_lineno
        line = linecache.getline(filename, line_code)

        if event == "return" and filename in self._context and line_code in self._context[filename]:
            self._context[filename][line_code]["flags"].append("return")

        if not in_current_file or event != "line": 
            return self.__call__

        if "def" not in line and "for" not in line and "return" not in line:
            data = FData(frame)
            stats = self._processor.get_stats(data)
            self._send.send_data(stats)

        return self.__call__



tracer = Tracer()
sys.setprofile(tracer.__call__)
sys.settrace(tracer.__call__)
time.sleep(0.1)

import test_files.other_test
import test_files.numpy_test

sys.settrace(None)
sys.setprofile(None)

start_time = time.perf_counter_ns()
x = 0

print("\n" * 10)
print(f"Time of first in for loop: {time.perf_counter_ns() - start_time}")
print("\n" * 10)
