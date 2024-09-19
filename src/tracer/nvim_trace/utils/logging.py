import logging
import linecache


class PackageLogger(logging.Logger):

    def __init__(self, log_level: int = logging.DEBUG):
        super().__init__("nvim_trace")
        self.setLevel(logging.DEBUG)

        self._log_level = log_level
        self._logger = logging.getLogger(__file__.__str__())

    def print_by_line(self, frame, event, time_needed):
        filename = frame.f_code.co_filename
        line_code = frame.f_lineno
        line = linecache.getline(filename, lineno=line_code).replace("\n","")
        c = {
            "exception": "\033[31m",
            "c_exception": "\033[31m",
            "call": "\033[32m",
            "c_call": "\033[33m",
            "return": "\033[36m",
            "c_return": "\033[35m",
            "line": "\033[34m", # ]]]]]]]]]
        }

        if "frozen" not in filename:
            print(f"[{time_needed: 9.1f}][ {c[event]}{event:^8s}\033[0m ]\033[37m ({line_code:^3d}): {line[:40]:<40s} \033[0m")  # ]]]
