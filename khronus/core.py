"""Core funtionality for khronus.."""

import os
import time
import functools

from strct.dicts import append_to_dict_val_list

from .util import mean
from .cfg import log_dpath


# === timing context ===

FUNCNAME_TO_RUNTIMES = {}


def get_time_log_fpath():
    fname = time.strftime("pgen-timelog-%Y%m%d-%H%M%S.log")
    return os.path.join(log_dpath(), fname)


def reset_time_logs():
    global FUNCNAME_TO_RUNTIMES
    FUNCNAME_TO_RUNTIMES = {}


def dump_time_logs(first_line=None, extra_timing_tuple=None):
    os.makedirs(log_dpath(), exist_ok=True)
    funcnames_counts_avg_runtimes = []
    for funcname, runtimes in FUNCNAME_TO_RUNTIMES.items():
        count = len(runtimes)
        avg = mean(runtimes)
        funcnames_counts_avg_runtimes.append((funcname, count, avg))
    if extra_timing_tuple:
        funcnames_counts_avg_runtimes.append(extra_timing_tuple)
    funcnames_counts_avg_runtimes = sorted(
        funcnames_counts_avg_runtimes, key=lambda x: x[2], reverse=True)
    lines = [
        (
            f"{funcname}  |  {avg_runtime:.2f}s avg running time  "
            f"| Ran {count} times.\n"
        )
        for funcname, count, avg_runtime in funcnames_counts_avg_runtimes
    ]
    if first_line:
        lines = [first_line] + lines
    fpath = get_time_log_fpath()
    with open(fpath, 'wt+') as f:
        f.writelines(lines)


def add_manual_entry(name, running_time):
    append_to_dict_val_list(
        dict_obj=FUNCNAME_TO_RUNTIMES,
        key=name,
        val=running_time,
    )


def decotimer(func):
    """Measures and logs the runnning time of a decorated function."""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.time()
        return_val = func(*args, **kwargs)
        end = time.time()
        running_time = end - start
        append_to_dict_val_list(
            dict_obj=FUNCNAME_TO_RUNTIMES,
            key=func.__name__,
            val=running_time,
        )
        return return_val
    return wrapper_timer
