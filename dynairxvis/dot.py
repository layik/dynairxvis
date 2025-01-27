import numpy as np
import matplotlib.pyplot as plt
from .utils import FIG_SIZE


def dot(values, fig_kw={}, ax_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a dot plot based on the provided values.

    Parameters
    ----------
    values : list of float
        The values to be plotted. Each unique value's occurrence count
        determines the number of dots plotted for that value.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
        Default is an empty dict. Example: {'figsize': (6, 4)}
    ax_kw : dict
        Keyword arguments for ax.set() to customize the Axes.
        Default is an empty dict. Example: {'ylim': (-1, max_count)}
    plot_kw : dict
        Additional keyword arguments to pass to ax.plot() for further
        customization.
    kwargs : dict
        Additional keyword arguments for other matplotlib customizations
        that might not fit into the above categories.

    Example
    -------
    values = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

    dot(values)
    """
    # Determine the counts for each unique value
    vs, counts = np.unique(values, return_counts=True)

    # Default figure and axes setup
    fig_defaults = FIG_SIZE
    fig_defaults.update(fig_kw)  # Update with any user-provided figure kwargs

    # Create figure and axes
    fig, ax = plt.subplots(**fig_defaults)

    # Default plot properties
    plot_defaults = {'marker': 'o', 'color': 'k', 'linestyle': '', 'ms': 10}
    plot_defaults.update(plot_kw)  # Update with any user-provided plot kwargs

    # Plotting the dots
    for value, count in zip(vs, counts):
        ax.plot([value]*count, list(range(count)), **plot_defaults, **kwargs)

    # Customizing the axes appearance
    ax_defaults = {
        'ylim': (-1, max(counts)),
        'spines.top': False, 'spines.right': False, 'spines.left': False,
        'yaxis.visible': False,
        'xaxis.tick_params': {'axis': 'x', 'length': 0, 'pad': 8, 
                              'labelsize': 12}
    }
    ax_defaults.update(ax_kw)  # Update with any user-provided axes kwargs

    # Apply the customizations
    for attr, value in ax_defaults.items():
        if hasattr(ax, attr):
            setattr(ax, attr, value)
        elif attr.startswith('spines.'):
            spine = attr.split('.')[1]
            ax.spines[spine].set_visible(value)
        elif attr == 'xaxis.tick_params':
            ax.tick_params(**value)

    plt.show()
