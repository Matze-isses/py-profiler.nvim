
def unit_value_trafo(value, units):
    num_given_units = len(units)
    if value < 1000:
        return value, units[-1]

    for i in range(num_given_units):
        comparetor = 10 ** (3 * (num_given_units - (i + 1))) - 1
        if value > comparetor-1:
            return value / comparetor if comparetor > 0 else 0, units[i]
    raise ValueError(f"{value} is smaller the 1! Cannot generate unit values")


def create_prints(time, calls):
    if calls == 0:
        return "‖     -    │     -     │     -     "
    time_s, unit_s = unit_value_trafo(time, ["s", "ms", "us", "ns", "ps"])
    calls_s, unit_c = unit_value_trafo(calls, ["B", "M", "K", " "])
    time_t, unit_t = unit_value_trafo(time*calls, ["s", "ms", "us", "ns", "ps"])

    return f"‖ {calls_s:> 6.1f}{unit_c:<1s}  │ {time_s:> 6.1f}{unit_s:>2s}  │ {time_t:> 6.1f}{unit_t:>2s}  "
