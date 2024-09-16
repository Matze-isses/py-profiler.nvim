from collections import deque
import sys
import os
import time
import json
import linecache

from formatting import create_prints


"""
The following observation will be useful:
    - Within the testfile the iteration over the array calls 10 times:

    rand_one = np.array([np.random.randint(1, i+5) line
    rand_one = np.array([np.random.randint(1, i+5) c_call
    rand_one = np.array([np.random.randint(1, i+5) c_return
"""

class Tracer:
    DEBUG = True

    def __init__(self, path: str = "/tmp/nvim_trace.json", filter_cwd: str = "", history_max = 3):
        self._path = path
        self._current_cwd = filter_cwd if filter_cwd != "" else os.getcwd()

        self._line_times = {}
        self.level = 1
        self._open = {}
        self._last_line = -1

    def _directory_filter(self, frame):
        name = frame.f_code.co_filename
        if not (type(name) is str and name.startswith(self._current_cwd)): return self.trace_calls
        return name

    def profile_calls(self, frame, event, arg):
        filename = self._directory_filter(frame)
        if type(filename) is not str: return filename

        if event == "call" or event == "return":
            return self.profile_calls

        return self.event_callback(frame, event)

    def trace_calls(self, frame, event, arg):
        filename = self._directory_filter(frame)
        if type(filename) is not str: return filename
        return self.event_callback(frame, event)


    def event_callback(self, frame, event, args=None):
        filename = frame.f_code.co_filename
        line_nr = frame.f_lineno
        key = (line_nr, filename)

        if key not in self._line_times and key not in self._open:
            self._line_times[key] = { 'start': 0, 'count': 0, 'time': 0.0 }
        
        if key in self._open and event in ["c_return", "return"]:
            start_time = self._open.pop(key)
            close_time = time.perf_counter_ns() - start_time
            self._line_times[key]["count"] += 1
            self._line_times[key]["time"] += close_time - self._line_times[key]["time"]
            self._last_line = line_nr
            return self.event_callback

        if event in ["line", "call"] and key not in self._open:
            self._open[key] = time.perf_counter_ns()

        self.debug_print(frame, event, False, filename)
        return self.trace_calls

    def profile_code(self, func):
        self._line_times = {}
        # Start tracing
        sys.setprofile(self.profile_calls)
        sys.settrace(self.trace_calls)

        func()

        sys.settrace(None)
        sys.setprofile(None)

        results = {}
        output = {}

        for (line_nr, filename), data in self._line_times.items():
            if not filename.startswith(self._current_cwd): continue
            if filename not in results: results[filename] = []
            if filename not in output:
                output[filename] = {}
            output[filename][line_nr] = create_prints(data['time'], data['count'])

        for filename, lines in output.items():
            max_line = max(lines.keys())
            for i in range(1, max_line):
                if i not in output[filename]: output[filename][i] = "‖     -    │     -     │     -     "

            output[filename] = {i-1: output[filename][i] for i in sorted(output[filename].keys())}

        # Write results to JSON
        with open(self._path, 'w') as f:
            json.dump(output, f, indent=2)

    def debug_print(self, frame, event, from_profiler, filename):
        if self.DEBUG:
            line_nr = frame.f_lineno
            line = linecache.getline(filename, lineno=line_nr).replace("\n","")
            c = {
                "exception": "\033[31m",
                "c_exception": "\033[31m",
                "call": "\033[32m",
                "c_call": "\033[33m",
                "return": "\033[36m",
                "c_return": "\033[35m",
                "line": "\033[34m",
            }
            print(f'{"P" if from_profiler else "T"}[ {c[event]}{event:^8s}\033[0m ]({line_nr:^3d}): {line[:50]:<50s}')
