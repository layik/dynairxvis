import os
import matplotlib.pyplot as plt
from .radar import radar
from .dot import dot
from .box import box
from .hist import histogram
from .gantt import gantt
from .scatter import scatter
from .heatmap import heatmap
from .bar import bar
from .pie import pie

# =============================================================================
# Internal
# =============================================================================
def _draw_fig(filename=None, overwrite=False, **kwargs):
    """
    Internal function, which is called to draw a plot to the screen or
    save it in a file.

    Parameters
    ----------
    filename : str, optional
        The filename for the figure. If None, the figure is displayed
        on the screen.
    overwrite : bool, optional
        If False, does not overwrite the file if it exists. If True,
        overwrites the file.
    **kwargs : dict
        Keyword arguments for fig.savefig().

    Returns
    -------
    None.
    """
    if filename is not None:
        if overwrite or not os.path.isfile(filename):
            fig = plt.gcf()
            fig.savefig(filename, **kwargs)
        else:
            print('** WARNING **: Figure not saved. File exists.')
            print(filename)
    else:
        plt.show()


def plot(plot_name, *args, **kwargs):
    """
    High-level plotting function that dispatches to specific plotting functions
    based on plot_name. It then shows the plot or saves it to a file.

    Parameters
    ----------
    plot_name : str
        The name of the plot type to generate.
    *args : tuple
        Positional arguments passed directly to the plotting function.
    **kwargs : dict
        Keyword arguments passed directly to the plotting function. It should
        include 'filename' and 'overwrite' if saving the plot is desired.

    Returns
    -------
    None.
    """
    # Extract filename and overwrite from kwargs, defaulting to None and False if not present
    filename = kwargs.pop('filename', None)
    overwrite = kwargs.pop('overwrite', False)

    # Mapping of plot_name to plotting function
    plot_functions = {
        'bar': bar,
        'box': box,
        'dot': dot,
        'gantt': gantt,
        'heatmap': heatmap,
        'hist': histogram,
        'pie': pie,
        'radar': radar,
        'scatter': scatter
    }

    if plot_name in plot_functions:
        # Create the plot
        plot_func = plot_functions[plot_name]
        # Ensure plot functions return fig, ax
        plot_func(*args, **kwargs)
    else:
        print(f"**WARNING: ** '{plot_name}' is not a supported plot type.")

    # Show the plot or save it to a file
    _draw_fig(filename=filename, overwrite=overwrite, **kwargs)
