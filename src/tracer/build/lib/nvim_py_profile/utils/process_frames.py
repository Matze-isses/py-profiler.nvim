from typing import Dict
from nvim_trace.utils.logging import PackageLogger
from nvim_trace.utils.line_data import FData
import traceback
import pstats
import profile
import time


class Processor:

    def __init__(self, logger: PackageLogger):
        self._logger = logger
        self._stats: Dict[str, pstats.Stats] = {}
        self._mapping = {}

    def get_stats(self, f_data: FData):
        try:
            if f_data.file_name not in self._stats:
                self._stats[f_data.file_name] = pstats.Stats()

            frame_profile = profile.Profile(timer=time.perf_counter_ns)
            frame_profile.runctx(f_data.code, f_data.frame.f_globals, f_data.frame.f_locals).create_stats()

            self._stats[f_data.file_name].add(frame_profile)
            line_vals = self._stats[f_data.file_name].get_stats_profile().func_profiles[f_data.code]
            return (f_data.file_name, f_data.line_nr, line_vals.percall_cumtime, line_vals.ncalls)
        except Exception:
            self._logger.critical(f"Could not get the stats from a frame! this is not supposed to happen and must be fixed, as it could end in unwanted systemwide behavior!\n\n{traceback.format_exc()}\n\n")
            raise ValueError("Error while processing frame!")

    def get_mapper(self):
        mapping = {key: value.get_stats_profile().func_profiles for key, value in self._stats.items()}

        def get_stats(file, line):
            return mapping[file][line]

        return get_stats

