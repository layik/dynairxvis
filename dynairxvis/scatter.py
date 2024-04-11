from .time import grouped_chart


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
    grouped_chart(categories, start_dates, end_dates, chart_type='scatter',
                  markers=markers, fig_kw=fig_kw, plot_kw=plot_kw, **kwargs)
