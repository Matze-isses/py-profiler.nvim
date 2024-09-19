import linecache


class FData:

    def __init__(self, frame):
        self.frame = frame
        self.line_nr = frame.f_lineno
        self.file_name = frame.f_code.co_filename 
        self.code = linecache.getline(self.file_name, self.line_nr).strip()
        self.cum_time, self.call_time, self.calls = None, None, None

    def add_stats(self, stats):
        self.call_time = stats.func_profiles[self.code].percall_tottime
        self.cum_time = stats.func_profiles[self.code].tottime
        self.calls = stats.func_profiles[self.code].ncalls
        return self


