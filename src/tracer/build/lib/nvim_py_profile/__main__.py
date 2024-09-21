import logging
import profile, pstats, io
import subprocess
import profile
import numpy as np
import time
import os
import sys
import linecache

from nvim_py_profile.sender import Sender
from nvim_py_profile.utils.logging import PackageLogger
from nvim_py_profile.utils.process_frames import Processor
from nvim_py_profile.utils.line_data import FData


def find_setup_py_or_fallback(path):
    two_levels_up = os.path.abspath(os.path.join(path, '..', '..'))
    while path != os.path.abspath(os.sep):
        if 'setup.py' in os.listdir(path):
            return path
        path = os.path.abspath(os.path.join(path, '..'))
    return two_levels_up


class Tracer:

    def __init__(self, script_of_interest):
        self._home_dir = find_setup_py_or_fallback("/".join(script_of_interest.split("/")[:-1]))
        self._logger = PackageLogger()
        self._logger.addHandler(logging.StreamHandler())
        self._processor = Processor(self._logger)
        self._send = Sender()
        self._recursion_level = 0
        self._max = 3
        self._context = {}

    def __call__(self, frame, event, args):
        in_current_file = frame.f_code.co_filename == os.path.abspath(self._home_dir)
        print(f"The current file is named: {frame.f_code.co_filename}")
        print(f"Current Working Directory: {os.path.abspath(os.getcwd())}")
        print(self._home_dir)

        if in_current_file and event != "line": 
            return self.__call__

        filename = frame.f_code.co_filename
        line_code = frame.f_lineno
        line = linecache.getline(filename, line_code)

        if "def" not in line and "for" not in line and "return" not in line:
            data = FData(frame)
            stats = self._processor.get_stats(data)
            self._send.send_data(stats)

        return self.__call__



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wrapper_script.py script_of_interest.py")
        sys.exit(1)

    script_of_interest = sys.argv[1]

    tracer = Tracer(script_of_interest)
    sys.settrace(tracer.__call__)
    sys.setprofile(tracer.__call__)
    print(f"Current Working Directory: {os.path.abspath(os.getcwd())}")
    exec(script_of_interest)
    sys.settrace(None)
    sys.setprofile(None)

