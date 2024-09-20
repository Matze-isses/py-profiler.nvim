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
        self._context = {}

    def __call__(self, frame, event, args):
        in_current_file = frame.f_code.co_filename.startswith("/home/admin/nvim/")

        if not in_current_file or event != "line": 
            return self.__call__

        filename = frame.f_code.co_filename
        line_code = frame.f_lineno
        line = linecache.getline(filename, line_code)

        if "def" not in line and "for" not in line and "return" not in line:
            data = FData(frame)
            stats = self._processor.get_stats(data)
            self._send.send_data(stats)

        return self.__call__



start_time = time.perf_counter_ns()
x = 0
tracer = Tracer()
sys.settrace(tracer.__call__)
sys.setprofile(tracer.__call__)



sys.settrace(None)
sys.setprofile(None)

print("\n" * 10)
print(f"Time of first in for loop: {time.perf_counter_ns() - start_time}")
print("\n" * 10)
