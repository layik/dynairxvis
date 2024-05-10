import numpy as np
import matplotlib.pyplot as plt
from .utils import FIG_SIZE


def violin(values, horizontal=False, fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a violin plot based on the provided values.

    Parameters
    ----------
      values : list of float
        The values to be included in the violin plot.
      horizontal : bool, optional
        Whether to display the violin plot horizontally. Defaults to False.
      fig_kw : dict
        Keyword arguments for plt.figure() to customize the figure.
      plot_kw : dict
        Keyword arguments for plt.violinplot() for further customization.
      **kwargs : dict
        Additional keyword arguments for customization.

      Example
      -------
      values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

      violin(values)
    """
    # Setup default figure size
    default_fig_kw = FIG_SIZE
    # Update with any user-provided figure kwargs
    default_fig_kw.update(fig_kw)

    # Setup figure with combined default and provided figure kwargs
    plt.figure(**default_fig_kw)

    # Setup default plot parameters for the violin plot
    default_plot_kw = {'showmeans': False, 'showmedians': True,
                       'showextrema': True}
    default_plot_kw.update(plot_kw)  # Update with any user kwargs

    # Plot the violin plot
    parts = plt.violinplot(values, vert=not horizontal, **default_plot_kw)

    # Apply a default grayscale color map if no color is provided in plot_kw
    colors = plot_kw.get('colors', None)
    if colors is None:
        colors = plt.cm.Greys(np.linspace(0.3, 0.7, len(parts['bodies'])))
    edgecolor = plot_kw.get('edgecolor', 'black')
    for part, color in zip(parts['bodies'], colors):
        part.set_facecolor(color)
        part.set_edgecolor(edgecolor)

    # Set the color of the 'cbars', 'cmins', and 'cmaxes' parts to black
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians'):
        vp = parts[partname]
        vp.set_edgecolor(edgecolor)

    plt.title(kwargs.get('title', 'Violin Plot of Values'))
    plt.ylabel(kwargs.get('ylabel', 'Values'))
    plt.xticks([1], kwargs.get('xticks_labels', ['Value Set']))
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)
    plt.show()
