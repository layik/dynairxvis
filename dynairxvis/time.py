import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import itertools


def grouped_chart(categories, start_dates, end_dates, chart_type='line',
                  markers=None, fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a grouped chart (line, scatter, or Gantt)
    based on the provided data.

    Parameters
    ----------
    categories : list of str
        Categories or names of the tasks.
    start_dates : list of datetime
        Start dates for each task.
    end_dates : list of datetime
        End dates for each task.
    chart_type : str, optional
        Type of chart to create ('line', 'scatter', 'gantt').
        Default is 'line'.
    markers : dict, optional
        Dictionary mapping categories to custom marker styles
        (for scatter plots).
        Default is None, which uses a predefined cycle of markers.
    fig_kw : dict, optional
        Keyword arguments for plt.subplots() to customize the figure.
    plot_kw : dict, optional
        Keyword arguments for ax.plot()/ax.scatter()/ax.barh()
        to customize the chart.
    **kwargs : dict
        Additional keyword arguments for customization not related
        to ax.plot()/ax.scatter()/ax.barh().
        This includes 'xlabel', 'title', any axis formatter settings,
        and 'legend'.

    Examples
    --------
    >>> categories = ['Task A', 'Task B', 'Task C']
    >>> start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
        datetime(2020, 8, 1)]
    >>> end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
        datetime(2020, 9, 1)]
    >>> markers = {'Task A': '^', 'Task B': 's', 'Task C': 'o'}
    >>> grouped_chart(categories, start_dates, end_dates, chart_type='scatter',
        markers=markers)
    """
    # Set default figure properties
    default_fig_kw = {'figsize': (6, 4)}
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    # Set default markers and cycle through them if not provided
    default_markers = ['o', '^', 's', '*', '+', 'x', 'D', 'h']

    # Assign unique y-positions based on categories
    unique_cats = sorted(set(categories), key=categories.index)
    category_positions = {category: pos for pos,
                          category in enumerate(unique_cats, start=1)}

    # Create a color palette with as many gray shades as
    # there are unique categories
    # Here, '0.1' avoids pure black and '0.9' avoids pure white.
    gray_color_palette = plt.cm.Greys(np.linspace(0.2, 0.8, len(unique_cats)))

    # Check if the user has provided a custom color mapping,
    # otherwise use the default gray shades
    if 'category_colors' not in kwargs or not kwargs['category_colors']:
        category_colors = {category: color for category,
                           color in zip(unique_cats, gray_color_palette)}
    else:
        category_colors = kwargs['category_colors']

    # If markers are not provided, create a cycling
    # iterator of default markers.
    if markers is None:
        marker_iter = itertools.cycle(default_markers)
        category_markers = {category:
                            next(marker_iter) for category in unique_cats}
    else:
        # Use the provided markers dictionary directly.
        category_markers = markers

    # Plotting functions with consistent color and marker
    def _plot_scatter(ax, category, start_date, end_date, position, plot_kw):
        ax.scatter([start_date, end_date], [position, position],
                   color=category_colors[category],
                   marker=category_markers[category], **plot_kw,
                   label=category if category not in plotted_cats else "")
        plotted_cats.add(category)

    def _plot_line(ax, category, start_date, end_date, position, plot_kw):
        ax.plot([start_date, end_date], [position, position],
                color=category_colors[category],
                marker=category_markers[category], **plot_kw,
                label=category if category not in plotted_cats else "")
        plotted_cats.add(category)

    # To keep track of which categories have been plotted
    plotted_cats = set()
    # Plot based on the specified chart type
    for start_date, end_date, category in zip(start_dates, end_dates,
                                              categories):
        position = category_positions[category]
        if chart_type == 'scatter':
            _plot_scatter(ax, category, start_date, end_date,
                          position, plot_kw)
        elif chart_type == 'line':
            _plot_line(ax, category, start_date, end_date,
                       position, plot_kw)

    # Set axis, legend, and show plot
    plt.yticks(range(1, len(unique_cats) + 1), unique_cats)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xlabel(kwargs.get('xlabel', 'Date'))
    plt.title(kwargs.get('title', f'{chart_type.capitalize()} Chart'))
    if kwargs.get('legend', True):
        ax.legend(title="Categories", loc="best")
    plt.tight_layout()
    plt.show()


def line(categories, start_dates, end_dates, markers=None, fig_kw={},
         plot_kw={}, **kwargs):
    """
    Creates and displays a line chart for a series of tasks or events
    defined by their categories and corresponding start and end dates.

    This function is a specialized use of the more general grouped_chart
    function, focusing specifically on generating line charts. Each task
    or event will be represented as a line segment on the chart.

    Parameters
    ----------
    categories : list of str
        The categories or names of the tasks/events. Each category represents
        a separate line segment on the chart.
    start_dates : list of datetime
        The start dates for each task/event. Each start date corresponds to
        the beginning of a line segment for its category.
    end_dates : list of datetime
        The end dates for each task/event. Each end date corresponds to the
        end of a line segment for its category.
    markers : dict, optional
        A dictionary mapping categories to custom marker styles that denote
        the start and end of each line segment. If not provided, a default
        marker will be used.
    fig_kw : dict, optional
        Keyword arguments for plt.subplots() to customize the figure's
        appearance. For example, `figsize` to alter the size of the figure.
    plot_kw : dict, optional
        Keyword arguments for the line plotting functionality (ax.plot())
        to customize the appearance of the line segments. For example,
        `linewidth` to change the width of the lines, `linestyle` to
        change the style of the lines.
    **kwargs : dict
        Additional keyword arguments for further customization of the chart.
        Includes options like 'xlabel', 'title', 'legend', and any axis
        formatter settings. For example, setting 'legend' to True will
        include a legend on the chart.

    Examples
    --------
    >>> categories = ['Task A', 'Task B', 'Task C']
    >>> start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
    datetime(2020, 8, 1)]
    >>> end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
    datetime(2020, 9, 1)]
    >>> markers = {'Task A': '^', 'Task B': 's', 'Task C': 'o'}
    >>> line(categories, start_dates, end_dates, markers=markers)
    """
    grouped_chart(categories, start_dates, end_dates, chart_type='line',
                  markers=markers, fig_kw=fig_kw, plot_kw=plot_kw, **kwargs)
