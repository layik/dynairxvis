import matplotlib.pyplot as plt
import numpy as np
from .time import grouped_chart
from .utils import FIG_SIZE


def scatter(categories, start_dates=None, end_dates=None, values=None,
            mode='gantt', orientation='vertical', markers=None, fig_kw={},
            plot_kw={}, **kwargs):
    """
    Creates and displays a scatter plot or bar chart with custom settings
    based on the mode specified.

    Parameters
    ----------
    categories : list of str
        The categories or names of the tasks or nominal categories on x-axis.
    values : list of int
        Quantitative values for each category.
    mode : str, optional
        Determines the type of plot:
        - 'gantt': Gantt-like plot using start_dates and end_dates.
        - 'scatter': Traditional scatter plot with values on y-axis.
        - 'bar': Bar chart with values represented as bars.
    orientation : str, optional
        Orientation of the bar chart if mode is 'bar'. Options are
        'vertical' or 'horizontal'.
    markers : dict, optional
        A dictionary mapping categories to custom marker styles.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
    plot_kw : dict
        Keyword arguments for ax.bar() or ax.scatter() to further
        customize the points or bars.
    **kwargs : dict
        Additional keyword arguments for customization not related to
        ax.scatter() or ax.bar().

    Example
    -------
    categories = ['Category A', 'Category B', 'Category C']
    values = [10, 20, 30]
    scatter(categories, values=values, mode='bar', orientation='horizontal')
    """
    if mode not in ['gantt', 'scatter', 'bar']:
        raise ValueError(
            "Invalid mode specified. Use 'gantt', 'scatter', or 'bar'.")

    if mode == 'gantt' and (start_dates is None or end_dates is None):
        raise ValueError(
            "Start and end dates must be provided for 'gantt' mode.")
    if mode == 'gantt':
        return grouped_chart(categories, start_dates, end_dates,
                             chart_type='scatter', markers=markers,
                             fig_kw=fig_kw, plot_kw=plot_kw, **kwargs)
    # start scatter/bar modes
    if values is None:
        raise ValueError(
            "Values must be provided for 'scatter' and 'bar' modes.")

    fig_defaults = FIG_SIZE
    fig_defaults.update(fig_kw)
    fig, ax = plt.subplots(**fig_defaults)

    x_indices = np.arange(len(categories))

    color_theme = kwargs.get('color_theme', ['black'] * len(categories))

    if mode == 'scatter':
        for i, value in enumerate(values):
            ax.scatter(x_indices[i], value,
                       marker=markers.get(
                           categories[i],
                           'o') if markers else 'o',
                       color=plot_kw.get('color', color_theme)[i],
                       **plot_kw)
    elif mode == 'bar':
        if orientation == 'horizontal':
            ax.barh(x_indices, values,
                    color=plot_kw.get('color', color_theme),
                    # remove color from kwargs
                    **{k: v for k, v in plot_kw.items() if k != 'color'})
        else:
            ax.bar(x_indices, values,
                   color=plot_kw.get('color', color_theme),
                   # remove color from kwargs
                   **{k: v for k, v in plot_kw.items() if k != 'color'})

    # Set category labels on x-axis or y-axis
    if orientation == 'horizontal' and mode == 'bar':
        ax.set_yticks(x_indices)
        ax.set_yticklabels(categories)
        ax.set_xlabel(kwargs.get('xlabel', 'Quantity'))
        ax.set_ylabel(kwargs.get('ylabel', ''))
    else:
        ax.set_xticks(x_indices)
        ax.set_xticklabels(categories)
        ax.set_ylabel(kwargs.get('ylabel', 'Quantity'))
        ax.set_xlabel(kwargs.get('xlabel', ''))

    ax.set_title(kwargs.get('title', f'{mode.capitalize()} Plot'))

    plt.tight_layout()
    plt.show()
