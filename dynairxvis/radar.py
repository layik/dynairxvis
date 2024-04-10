import numpy as np
import matplotlib.pyplot as plt


def radar(categories, values, fig_kw={}, ax_kw={}, **kwargs):
    """
    Creates and displays a radar chart based on
    the provided categories and values.

    Parameters
    ----------
    categories : list of str
        The categories to be plotted on the radar chart.
        Each category corresponds to one spoke on the radar chart.
    values : list of float
        The values for each category. Each value determines
        the distance from the center of the chart for
        its corresponding category.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
        Default is an empty dict. Example: {'figsize': (6, 4)}
    ax_kw : dict
        Keyword arguments for ax.set() to customize the Axes.
        Default is an empty dict. Example: {'title': 'Radar Chart'}
    kwargs : dict
        Additional keyword arguments to pass to ax.fill() and ax.plot()
        for further customization.

    Example
    -------
    categories = ['N1', 'N2', 'N3']
    values = [10, 15, 35]

    radar(categories, values)
    """
    # Copy the input lists to avoid modifying the originals
    categories_copy = categories[:]
    # Correctly closes the loop for plotting.
    values_copy = values[:] + [values[0]]

    # Number of variables we're plotting.
    num_vars = len(categories_copy)

    # Compute angle each bar is centered on:
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop for angles as well

    # Default figure and axes setup
    fig_defaults = {'figsize': (6, 4)}
    fig_defaults.update(fig_kw)  # Update with any user-provided figure kwargs

    # Plot
    fig, ax = plt.subplots(subplot_kw=dict(polar=True), **fig_defaults)
    ax.fill(angles, values_copy, color='gray', alpha=0.25, **kwargs)
    ax.plot(angles, values_copy, color='gray', linewidth=2, **kwargs)

    # Axes customizations
    ax_defaults = {'title': 'Radar Chart', 'yticklabels': [], 'xticks':
                   angles[:-1], 'xticklabels': categories_copy}
    ax_defaults.update(ax_kw)  # Update with any user-provided axes kwargs
    ax.set(**ax_defaults)

    plt.show()
