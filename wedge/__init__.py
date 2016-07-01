__version__ = "0.0.1.dev0"
__author__ = "Prajwal Kafle (prrajkafle@gmail.com)"
__copyright__ = "Copyright 2016-2017 Prajwal R. Kafle and contributors"
__contributors__ = [
    "Prajwal Kafle @pythonomer"
]

try:
    __WEDGE_SETUP__
except NameError:
    __WEDGE_SETUP__ = False

if not __WEDGE_SETUP__:
    __all__ = ["wedge"]
    from .wedge import cone
