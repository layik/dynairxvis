import matplotlib.pyplot as plt
from collections import defaultdict
from .utils import is_valid_array
import numpy as np
import pandas as pd

gray_color_palette = ['grey', 'none']


def pie(categories, values=None, time=False, start_dates=None,
        end_dates=None, fig_kw={}, **kwargs):
    """
    Creates and displays a grid of pie charts for given categories
    and associated values, or time-based intervals if time=True.

    Parameters
    ----------
    categories : list of str
        The categories for each pie chart.
    values : list of int or float, optional
        The values associated with each category.
    time : bool
        If True, uses start_dates and end_dates to create time-based
        pie charts.
    start_dates, end_dates : list of datetime, optional
        Lists of start and end dates for each category if time=True.
    fig_kw : dict, optional
        Keyword arguments for plt.subplots() to customize the figure.
    **kwargs : dict
        Additional keyword arguments for customization such as 'startangle',
        and 'colors'.

    Examples
    --------
    >>> categories = ['Category A', 'Category B', 'Category C']
    >>> values = [10, 20, 30]
    >>> pie(categories, values)
    """
    if time:
        if not is_valid_array(start_dates):
            raise ValueError("start_dates must be a valid array.")
        if not is_valid_array(end_dates):
            raise ValueError("end_dates must be a valid array.")
        if len(start_dates) != len(end_dates):
            raise ValueError(
                "start_dates and end_dates must have equal lengths.")
        return _grouped_pie(categories, start_dates, end_dates,
                            fig_kw=fig_kw, **kwargs)
    else:
        return _pie(categories, values, fig_kw=fig_kw, **kwargs)


def _show():
    plt.tight_layout()
    plt.show()


def _figure_and_axes(num_plots, fig_kw, **kwargs):
    """
    Creates a figure and the corresponding axes based on the number of plots.

    Parameters:
    num_plots (int): The number of plots (subplots) required.
    fig_kw (dict): Figure configuration parameters.

    Returns:
    tuple: The figure and axes objects.
    """
    # Set default figure properties
    default_fig_kw = {'figsize': (num_plots * 3, 3) if num_plots else (3, 3)}
    default_fig_kw.update(fig_kw)

    # Create figure and axes
    fig, axs = plt.subplots(1, max(num_plots, 1), **default_fig_kw, **kwargs)

    # Ensure axs is iterable, especially when there's only one plot
    if num_plots == 1:
        axs = [axs]  # Make it iterable if there's only one subplot

    return fig, axs


def _pie(categories, values, fig_kw, **kwargs):
    """
    Creates and displays pie charts based on the provided categories
    and values. If quantitative values are not provided, a single pie chart
    with equal segments is displayed.

    Parameters
    ----------
    categories : list of str
        The categories for the pie charts.
    values : list of int or float, optional
        The values associated with each category. If not provided, equal
        segments are created.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
    **kwargs : dict
        Additional keyword arguments for customization such as 'startangle',
        and 'colors'.
    """
    if not is_valid_array(categories):
        raise ValueError("categories must be a valid array.")

    # If values are not provided, create equal segments for a single pie chart
    if values is None:
        num_pies = 1
        total = len(categories)
        values_1pie = [1] * total
    else:
        if not is_valid_array(values):
            raise ValueError("values must be a valid array.")
        if len(categories) != len(values):
            raise ValueError("categories and values must have equal lengths.")
        num_pies = len(categories)
        total = sum(values)

    if values is None:
        # Plot a single pie chart with equal segments
        fig, ax = plt.subplots(**fig_kw)
        colors = plt.cm.Greys(np.linspace(0.2, 0.8, total))
        ax.pie(values_1pie, labels=categories if total < 10 else None,
               colors=colors, startangle=90, autopct='%1.1f%%',
               wedgeprops=dict(edgecolor='black'))
        if total >= 10:
            ax.legend(categories, loc="best", fontsize=8)
        # ax.set_title('Pie Chart')
    else:
        fig, axs = _figure_and_axes(num_pies, fig_kw)
        # Create a pie chart for each category
        for ax, category, value in zip(axs, categories, values):
            # Calculate pie segments
            segment = [value / total, (total - value) / total]
            # Plot pie chart
            ax.pie(segment, labels=[f'{value}', ''], colors=gray_color_palette,
                   startangle=90, wedgeprops=dict(edgecolor='black'),
                   normalize=True, **kwargs)
            ax.set_title(category)

    _show()


def _grouped_pie(categories, start_dates, end_dates, fig_kw={}, **kwargs):
    # Group intervals by category
    intervals_by_category = defaultdict(list)
    for category, start, end in zip(categories, start_dates, end_dates):
        intervals_by_category[category].append((start, end))

    num_categories = len(intervals_by_category)
    fig, axs = _figure_and_axes(num_categories, fig_kw, **kwargs)

    # Base date for normalization and plotting
    min_date = min(start_dates)
    max_date = max(end_dates)
    total_duration = (max_date - min_date).total_seconds()

    for ax, (category, intervals) in zip(axs, intervals_by_category.items()):
        wedges = []
        labels = []
        for start, end in intervals:
            start_sec = (start - min_date).total_seconds()
            end_sec = (end - min_date).total_seconds()
            start_angle = (start_sec / total_duration) * 360
            extent = ((end_sec - start_sec) / total_duration) * 360
            wedges.append((start_angle, extent))
            labels.append(f"{start.strftime('%Y-%m-%d')}\n{end.strftime('%Y-%m-%d')}")
        wedges.sort()
        # Plot the pie chart with the start and end dates as labels
        for i, (start_angle, extent) in enumerate(wedges):
            ax.pie([extent, 360 - extent], colors=gray_color_palette,
                   startangle=start_angle + 90, counterclock=False,
                   wedgeprops={'edgecolor': 'black'},
                   labels=[labels[i], ''], labeldistance=0.8)

        ax.set_title(category)

    _show()


def table_list(data, **kwargs):
    """
    Print a DataFrame, list, or series as a list with the column name in
    bold and underlined.

    Parameters
    ----------
    data : pandas.DataFrame, list, or pandas.Series
        The data to print.

    **kwargs : dict
        Additional keyword arguments for customization such as 'colormap',
        'cellLoc', 'rowLabels', 'colLabels', 'loc', 'bbox', 'cellColours',
        'cellLoc', 'rowColours', 'rowLoc', 'fontsize
    """
    if data is None:
        raise ValueError("data cannot be None.")

    # Convert list or series to DataFrame
    if isinstance(data, (list, pd.Series)):
        data = pd.DataFrame(data)

    # ANSI escape code for bold and underline
    BOLD_UNDERLINE = '\033[1m\033[4m'
    END = '\033[0m'

    # Print the column name in bold and underlined
    print(f"{BOLD_UNDERLINE}{data.columns[0]}{END}")

    # Print the DataFrame without the index, left-aligned
    max_width = max(data[data.columns[0]].astype(str).map(len))
    for index, row in data.iterrows():
        value = row[data.columns[0]]
        print(str(value).ljust(max_width, **kwargs))
