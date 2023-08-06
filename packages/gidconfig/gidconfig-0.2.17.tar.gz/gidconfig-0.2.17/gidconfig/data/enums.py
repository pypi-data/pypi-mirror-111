# region [Imports]


# * Standard Library Imports -->
from enum import Enum, Flag, auto

# * Gid Imports -->
import gidlogger as glog

# endregion [Imports]

__updated__ = '2020-11-14 14:54:23'

# region [Logging]

log = glog.aux_library_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


class Cfg(Flag):
    User = auto()
    Solid = auto()
    Database = auto()
    DefaultFolder = auto()


class Get(Enum):
    basic = auto()
    boolean = auto()
    int = auto()
    list = auto()
    path = auto()
    datetime = auto()


class Fallback(Enum):
    NULL = auto()


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
