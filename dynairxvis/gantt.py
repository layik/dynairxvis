import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

from .utils import FIG_SIZE, get_color_palette


def gantt(categories, start_dates, end_dates, bar_colors=None, fig_kw={},
          plot_kw={}, **kwargs):
    """
    Creates and displays a Gantt chart based on the provided categories
    and date ranges.

    Parameters
    ----------
    categories : list of str
        The categories or names of the categorical list.
    start_dates : list of datetime
        The start dates for each category.
    end_dates : list of datetime
        The end dates for each category.
    bar_colors : list of str, optional
        The colors for each bar in the Gantt chart. If not provided, default
        colors will be used.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
    plot_kw : dict
        Keyword arguments for ax.barh() to further customize the bars.
    **kwargs : dict
        Additional keyword arguments for customization
        not related to ax.barh(). This includes 'xlabel', 'title',
        and any axis formatter settings.

    Example
    -------
    gantt(categories=['Task A', 'Task B', 'Task C'],
          start_dates=[datetime(2020, 1, 1), datetime(2020, 6, 1),
          datetime(2020, 8, 1)],
          end_dates=[datetime(2021, 1, 1), datetime(2020, 7, 1),
          datetime(2020, 9, 1)],
          bar_colors=['red', 'green', 'blue'])
    """
    # Set up default figure settings
    default_fig_kw = FIG_SIZE
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    # If bar_colors is not provided, generate a color map based on the unique
    # categories
    if bar_colors is None:
        unique_cats = list(set(categories))
        unique_colors = dict(zip(unique_cats,
                                 get_color_palette(len(unique_cats))))
    else:
        unique_cats = list(set(bar_colors))
        unique_colors = dict(zip(unique_cats,
                                 get_color_palette(len(unique_cats))))
    print(unique_cats)
    # Plot each task using the provided plot kwargs
    legend_patches = []
    for i, (category, start, end) in enumerate(zip(categories, start_dates,
                                                   end_dates)):
        color_key = (bar_colors[i]
                     if bar_colors is not None and not bar_colors.empty
                     else category)
        color = unique_colors.get(color_key, 'black')
        ax.barh(category, end - start, left=start,
                height=0.4, color=color, edgecolor='black', **plot_kw)
        legend_patches.append(Patch(color=color, label=color_key))

    # Set the x-axis to use a date format, if not overridden by kwargs
    if not kwargs.get('suppress_date_format'):
        ax.xaxis_date()
        myFmt = kwargs.get('date_formatter', mdates.DateFormatter('%Y'))
        ax.xaxis.set_major_formatter(myFmt)

    # Set x-axis limits if not provided in kwargs
    if not kwargs.get('xlim'):
        ax.set_xlim(
            [min(start_dates) - (max(end_dates) - min(start_dates)) / 10,
             max(end_dates) + (max(end_dates) - min(start_dates)) / 10])

    # Add grid, labels, and title using kwargs
    ax.grid(True)
    plt.xlabel(kwargs.get('xlabel', 'Time'))
    plt.title(kwargs.get('title', 'Gantt Chart'))

    # Add legend if bar_colors is provided
    if bar_colors is not None and not bar_colors.empty:
        plt.legend(handles=legend_patches, title='bar_colors')

    plt.tight_layout()
    plt.show()

    # Return figure and axes for further manipulation if needed
    return fig, ax
