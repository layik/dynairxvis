import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import itertools


def scatter(categories, start_dates, end_dates, markers=None, fig_kw={},
            plot_kw={}, **kwargs):
    """
    Creates and displays a grouped scatter plot with custom markers
    for each category.

    Parameters
    ----------
    categories : list of str
        The categories or names of the tasks.
    start_dates : list of datetime
        The start dates for each task.
    end_dates : list of datetime
        The end dates for each task.
 markers : dict, optional
        A dictionary mapping categories to custom marker styles.
        If not provided, default markers will be cycled through
        for each category.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
    plot_kw : dict
        Keyword arguments for ax.scatter() to further customize
        the scatter points.
    **kwargs : dict
        Additional keyword arguments for customization
        not related to ax.scatter().
        This includes 'xlabel', 'title', and any axis formatter settings.

    Example
    -------
    categories = ['Task A', 'Task B', 'Task C']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
    datetime(2020, 8, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
    datetime(2020, 9, 1)]
    markers = {'Task A': '^', 'Task B': 's', 'Task C': 'o'}

    scatter(categories, start_dates, end_dates, markers)
    """
    # Default figure and plot settings
    default_fig_kw = {'figsize': (6, 4)}
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    default_markers = ['o', '^', 's', '*', '+', 'x', 'D', 'h']
    marker_cycle = itertools.cycle(default_markers)

    if markers is None:
        markers = {}

    unique_categories = sorted(set(categories), key=categories.index)
    category_positions = {category: pos for pos, category in enumerate(unique_categories, start=1)}

    for start_date, end_date, category in zip(start_dates, end_dates, categories):
        y_position = category_positions[category]
        marker = markers.get(category, next(marker_cycle))
        ax.scatter([start_date, end_date], [y_position, y_position],
                   marker=marker, **plot_kw, label=category if kwargs.get('legend', True) else "")

    plt.yticks(list(category_positions.values()), unique_categories)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel(kwargs.get('xlabel', 'Time'))
    plt.title(kwargs.get('title', 'Grouped Scatter Chart with Custom Markers'))

    # Conditionally display the legend based on 'legend' in kwargs
    if kwargs.get('legend', True):
        ax.legend(title="Categories", loc="best")

    plt.tight_layout()
    plt.show()
