import tomli
import os

from .dot import dot
from .box import box
from .bar import bar
from .pie import pie, table_list
from .time import line
from .gantt import gantt
from .radar import radar
from .violin import violin
from .hist import histogram
from .scatter import scatter
from .heatmap import heatmap
from .calendar import calendar
from .utils import profile, findIndex


def get_version():
    # Dynamically fetch version from pyproject.toml
    pyproject_path = os.path.join(
        os.path.dirname(__file__), "..", "pyproject.toml")
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
    return pyproject_data["tool"]["poetry"]["version"]


__version__ = get_version()
__author__ = 'Dynairx'

__all__ = [
    'dot', 'box', 'bar', 'pie', 'table_list', 'line', 'gantt', 'radar',
    'violin', 'histogram', 'scatter', 'heatmap', 'calendar', 'profile',
    'findIndex'
]
