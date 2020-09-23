"""Configuration for khronus."""

from birch import Birch


CFG = Birch('khronus')


LOG_DPATH_KEY = 'LOG_DPATH'


def log_dpath():
    try:
        return CFG[LOG_DPATH_KEY]
    except KeyError:
        return CFG.xdg_cache_dpath()
