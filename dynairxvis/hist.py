import matplotlib.pyplot as plt
from .utils import FIG_SIZE, resolve_orientation


def histogram(values, bins=None, orientation='vertical',
              fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a histogram based on the provided values.

    Parameters
    ----------
    values : list of float
        The values to be included in the histogram.
    bins : list of int, optional
        The bin edges for the histogram. If None, default bin edges are used.
    orientation : str, optional
        The orientation of the histogram ('vertical' or 'horizontal').
    fig_kw : dict
        Keyword arguments for plt.figure() to customize the figure.
        Uses {'figsize': (6, 4)} as default.
    plot_kw : dict
        Keyword arguments for plt.hist() for further customization.
    **kwargs : dict
        Additional keyword arguments for customization
        not related to plt.hist().

    Example
    -------
    histogram(values, bins=[0, 2, 4, 6, 8, 10], orientation='horizontal',
              xlabel='Frequency', ylabel='Value')
    """
    # resolve orientation
    orientation = resolve_orientation(orientation)

    # Setup default figure size
    default_fig_kw = FIG_SIZE.copy()  # Ensure FIG_SIZE remains unchanged
    default_fig_kw.update(fig_kw)  # Merge user-provided fig_kw

    # Setup figure
    plt.figure(**default_fig_kw)

    # Set default plot properties
    plot_defaults = {'edgecolor': 'black', 'color': 'gray'}
    plot_defaults.update(plot_kw)  # Merge user-provided plot_kw

    # Plot the histogram
    plt.hist(values, bins=bins, orientation=orientation, **plot_defaults)

    # Dynamically adjust labels based on orientation
    if orientation == 'horizontal':
        plt.xlabel(kwargs.get('xlabel', 'Frequency'))  # xlabel gets 'ylabel'
        plt.ylabel(kwargs.get('ylabel', 'Value'))      # ylabel gets 'xlabel'
    else:
        plt.xlabel(kwargs.get('xlabel', 'Value'))
        plt.ylabel(kwargs.get('ylabel', 'Frequency'))

    # Title setup if provided
    plt.title(kwargs.get('title', 'Histogram of Values'))

    # Adjust tick marks if specified in kwargs
    if 'xticks' in kwargs and 'xticklabels' in kwargs:
        if orientation == 'horizontal':
            plt.yticks(kwargs['xticks'], kwargs['xticklabels'])
        else:
            plt.xticks(kwargs['xticks'], kwargs['xticklabels'])

    # Show the figure
    plt.show()
