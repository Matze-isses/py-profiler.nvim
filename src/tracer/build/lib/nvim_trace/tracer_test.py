from argparse import Namespace
import profile, pstats, io
from pstats import SortKey
import profile
import types
import inspect
import timeit
import numpy as np
import os
import time
import sys
import linecache

import logging
from nvim_trace.logging import Logger



class Tracer:

    def __init__(self):
        self._logger = Logger(logging.DEBUG)
        self._recursion_level = 0
        self._max = 3
        self._times = [("", 0)]

        self.pending_lines = []
        self._context = {}
        self._call_counting = {}
        self.always_in_vars = {}
        self._vars_before = {}
        self.profile = profile.Profile(timer=time.perf_counter_ns)

    def __call__(self, frame, event, args):
        in_current_file = frame.f_code.co_filename.startswith("/home/admin/projects/tracer")
        
        filename = frame.f_code.co_filename
        line_code = frame.f_lineno
        line = linecache.getline(filename, line_code)

        if event == "return" and filename in self._context and line_code in self._context[filename]:
            self._context[filename][line_code]["flags"].append("return")

        if not in_current_file or event != "line": 
            return self.__call__


        if filename not in self._context:
            self._context[filename] = {}
            self._call_counting[filename] = 0

        if line_code not in self._context[filename]:
            self._call_counting[filename] += 1

        if "def" not in line and "for" not in line and "return" not in line:
            self.profile = profile.Profile(timer=time.perf_counter_ns)
            self.profile.runctx(line.strip(), frame.f_globals, frame.f_locals).create_stats()
            val = pstats.Stats(self.profile).get_stats_profile()
            time_exec = val.func_profiles[line.strip()].percall_tottime
            self._logger.print_by_line(frame, event, False, time_exec)

        return self.__call__

    def create_setup_func(self, params):
        def setup():
            local_vars = globals()
            local_vars.update(params)
        return setup


tracer = Tracer()
sys.setprofile(tracer.__call__)
sys.settrace(tracer.__call__)
time.sleep(0.1)

import test_files.other_test
import test_files.numpy_test

sys.settrace(None)
sys.setprofile(None)

tracer.print()

start_time = time.perf_counter_ns()
x = 0

print("\n" * 10)
print(f"Time of first in for loop: {time.perf_counter_ns() - start_time}")
print("\n" * 10)
