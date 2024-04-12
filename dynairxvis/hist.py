import matplotlib.pyplot as plt
from .utils import FIG_SIZE


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
    # Setup default figure size
    default_fig_kw = FIG_SIZE
    # Update with any user-provided figure kwargs,
    # preserving the defaults unless overridden
    default_fig_kw.update(fig_kw)

    # Setup figure with combined default and provided figure kwargs
    plt.figure(**default_fig_kw)

    # Set default plot properties
    plot_defaults = {'edgecolor': 'black', 'color': 'gray'}
    # Update with any user-provided plot kwargs,
    # preserving the defaults unless overridden
    plot_defaults.update(plot_kw)

    # Plot the histogram
    plt.hist(values, bins=bins, orientation=orientation, **plot_defaults)

    # Dynamically adjust labels based on orientation
    if orientation == 'horizontal':
        plt.ylabel(kwargs.get('xlabel', 'Value'))
        plt.xlabel(kwargs.get('ylabel', 'Frequency'))
    else:
        plt.xlabel(kwargs.get('xlabel', 'Value'))
        plt.ylabel(kwargs.get('ylabel', 'Frequency'))

    # Title setup if provided
    plt.title(kwargs.get('title', 'Histogram of Values'))

    # Adjust tick marks if specified in kwargs, considering orientation
    if 'xticks' in kwargs and 'xticklabels' in kwargs:
        if orientation == 'horizontal':
            plt.yticks(kwargs['xticks'], kwargs['xticklabels'])
        else:
            plt.xticks(kwargs['xticks'], kwargs['xticklabels'])

    plt.show()
