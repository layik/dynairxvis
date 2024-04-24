import numpy as np
import matplotlib.pyplot as plt
from .time import grouped_chart


def heatmap(categories, values=None, start_dates=None, end_dates=None,
            mode='heatmap', fig_kw={}, cmap='Greys', **kwargs):
    """
    Creates and displays a heatmap for given categories
    and associated values or time intervals.

    Parameters
    ----------
    categories : list of str
        The categories for the y-axis of the heatmap.
    values : list of int or float, as flat or nested list (for 'value' mode).
        The values associated with each category.
    start_dates, end_dates : list of datetime (for 'time' mode)
        Start and end dates for each category interval.
    mode : str, optional
        'heatmap' for a standard value-based heatmap,
        'gantt' for a time-interval based heatmap.
    fig_kw : dict, optional
        Keyword arguments for plt.subplots() to customize the figure.
    cmap : str or Colormap, optional
        The colormap to use for the heatmap.
    **kwargs : dict
        Additional keyword arguments for customization such as 'xlabel',
        'ylabel', 'title', and 'colorbar'.

    Examples
    --------
    >>> categories = ['Category 1', 'Category 2', 'Category 3']
    >>> values = [1, 2, 3]
    >>> heatmap(categories, values=values, mode='value')
    >>> start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
        datetime(2020, 8, 1)]
    >>> end_dates = [datetime(2020, 3, 1), datetime(2020, 9, 1),
        datetime(2020, 12, 1)]
    >>> heatmap(categories, start_dates=start_dates, end_dates=end_dates,
        mode='gantt')
    """
    if mode not in ['gantt', 'heatmap']:
        raise ValueError(
            "Invalid mode specified. Use 'heatmap' or 'gantt'.")

    if mode == 'gantt' and (start_dates is None or end_dates is None):
        raise ValueError(
            "Start and end dates must be provided for 'gantt' mode.")
    if mode == 'gantt':
        return grouped_chart(categories, start_dates, end_dates,
                             chart_type='heatmap', fig_kw=fig_kw, **kwargs)

    # Improved flattening function that checks type of each item
    def flatten(values):
        flattened_values = []
        for item in values:
            if isinstance(item, list):
                flattened_values.extend(item)
            else:
                flattened_values.append(item)
        return flattened_values

    # Determine if values are nested and find unique values
    flattened_values = flatten(values)
    unique_values = sorted(set(flattened_values))
    heatmap_matrix = np.zeros((len(categories), len(unique_values)))

    # Fill the heatmap matrix
    for i, item in enumerate(values):
        if not isinstance(item, list):
            item = [item]  # Treat single values as list
        for value in item:
            value_index = unique_values.index(value)
            heatmap_matrix[i, value_index] += 1  # Increment for occurrences

    # Set default figure properties
    default_fig_kw = {'figsize': (5, len(categories))}
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    # Create the heatmap
    cax = ax.matshow(heatmap_matrix, cmap=cmap, aspect='auto')

    # Set ticks and labels
    ax.set_xticks(np.arange(len(unique_values)))
    ax.set_xticklabels(unique_values)
    ax.set_yticks(np.arange(len(categories)))
    ax.set_yticklabels(categories)

    # Move x-ticks to the top if preferred
    if kwargs.get('xticks_top', False):
        ax.xaxis.set_ticks_position('top')

    # Set axis labels and title
    ax.set_ylabel(kwargs.get('ylabel', 'Categories'))
    ax.set_title(kwargs.get('title', 'Heatmap'))

    # Colorbar settings if needed
    if kwargs.get('colorbar', False):
        fig.colorbar(cax, ax=ax, orientation='vertical')

    # Additional plot adjustments
    plt.tight_layout()
    plt.show()
