__version__ = '0.2.0'

from .parser import Parser
from .vectorizer import Vectorizer
from .stat_utils import Statist
from .matplotlib_utils import init_matplotlib
from .logger import get_logger
init_matplotlib()
