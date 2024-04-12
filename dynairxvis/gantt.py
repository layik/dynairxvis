import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from .utils import FIG_SIZE


def gantt(categories, start_dates, end_dates, fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a Gantt chart based on the provided task categories
    and date ranges.

    Parameters
    ----------
    categories : list of str
        The categories or names of the tasks.
    start_dates : list of datetime
        The start dates for each task.
    end_dates : list of datetime
        The end dates for each task.
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
          datetime(2020, 9, 1)])
    """
    # Set up default figure settings
    default_fig_kw = FIG_SIZE
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    # This could also be moved to plot_kw or kwargs if customization is desired
    colors = kwargs.get('colors',
                        ['lightgrey', 'darkgrey', 'darkgrey', 'black'])

    # Plot each task using the provided plot kwargs
    for i, (category, start, end) in enumerate(zip(categories,
                                                   start_dates, end_dates)):
        ax.barh(category, end - start, left=start,
                height=0.4, color=colors[i % len(colors)],
                edgecolor='black', **plot_kw)

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

    plt.tight_layout()
    plt.show()

    # Return figure and axes for further manipulation if needed
    return fig, ax
