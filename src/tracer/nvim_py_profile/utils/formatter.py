import numpy as np

units = ["ns", "us", "ms", "s ", "ks", "Ms"]


def formatting_output(time):
    unit = 0
    time_string = str(int(time))

    while len(time_string) >= 4:
        time_string = time_string[:-3]
        unit += 1
    return f"{time_string: >4s} {units[unit]}"


