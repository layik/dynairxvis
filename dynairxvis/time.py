import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import itertools
from .utils import FIG_SIZE


def grouped_chart(categories, start_dates, end_dates, chart_type='line',
                  values=None, markers=None, ax=None, fig_kw={},
                  plot_kw={}, **kwargs):
    """
    Creates and displays a grouped chart (line, scatter, or Gantt)
    based on the provided data.

    Parameters
    ----------
    categories : list of str
        Categories or names.
    start_dates : list of datetime
        Start dates for each task.
    end_dates : list of datetime
        End dates for each task.
    chart_type : str, optional
        Type of chart to create ('line', 'scatter', 'gantt').
        Default is 'line'.
    values : array-like, optional
        An optional array of numeric or ordered categorical values used to
        determine the color intensity or shade of the plot elements.
    markers : dict, optional
        Dictionary mapping categories to custom marker styles
        (for scatter plots).
        Default is None, which uses a predefined cycle of markers.
    ax : matplotlib.axes.Axes, optional. If provided, the `ax` object
        will be used to create the chart. Otherwise, a new figure and
        axes will be created.
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
    # validate chart type
    if chart_type not in ['line', 'scatter', 'heatmap']:
        print(f"Error: Invalid chart type '{chart_type}'. "
              "Choose from 'line', 'scatter', or 'heatmap'.")
        return
    # TODO: other input validations

    if isinstance(categories, pd.Series):
        categories = categories.tolist()

    # Set default figure properties
    default_fig_kw = FIG_SIZE
    default_fig_kw.update(fig_kw)
    if ax is None:
        fig, ax = plt.subplots(**default_fig_kw)

    unique_cats = sorted(set(categories), key=categories.index)
    category_colors = _get_cat_cols(categories, values, kwargs)

    # category_colors = kwargs.get('category_colors',
    #                              {cat: color for cat, color in zip(
    #                                  unique_cats, gray_color_palette)})
    default_markers = ['o', '^', 's', '*', '+', 'x', 'D', 'h']
    marker_cycle = itertools.cycle(default_markers)
    category_markers = markers or {
        cat: next(marker_cycle) for cat in unique_cats}

    # To keep track of which categories have been plotted
    plotted_cats = set()
    category_positions = {cat: i + 1 for i, cat in enumerate(unique_cats)}

    # Function to plot scatter and line plots
    def _plot_scatter_or_line():
        for start, end, cat in zip(start_dates, end_dates, categories):
            position = category_positions[cat]
            color = category_colors[cat]
            marker = category_markers[cat]
            if chart_type == 'scatter':
                ax.scatter([start, end], [position, position], color=color,
                           marker=marker, **plot_kw,
                           label=cat if cat not in plotted_cats else "")
            elif chart_type == 'line':
                ax.plot([start, end], [position, position], color=color,
                        marker=marker, **plot_kw,
                        label=cat if cat not in plotted_cats else "")
            plotted_cats.add(cat)

    def _plot_heatmap():
        # Determine time bins
        min_date, max_date = min(start_dates), max(end_dates)
        total_days = (max_date - min_date).days
        # Increase num_bins based on total duration in days for better
        # granularity
        # Example: ~1 bin per month if possible
        num_bins = max(10, total_days // 30)

        time_bins = np.linspace(mdates.date2num(min_date),
                                mdates.date2num(max_date), num_bins + 1)

        # Create heatmap data
        heatmap_data = np.zeros((len(unique_cats), num_bins))
        for start, end, cat in zip(start_dates, end_dates, categories):
            cat_idx = unique_cats.index(cat)
            start_idx = np.searchsorted(time_bins, mdates.date2num(start)) - 1
            end_idx = np.searchsorted(time_bins, mdates.date2num(end)) - 1
            # Fill all bins between start_idx and end_idx
            heatmap_data[cat_idx,
                         max(0, start_idx):min(end_idx + 1, num_bins)] = 1

        # Plotting the heatmap
        ax.imshow(heatmap_data, aspect='auto', cmap='Greys',
                  extent=[mdates.num2date(time_bins[0]),
                          mdates.num2date(time_bins[-1]), 0,
                          len(unique_cats)], origin='lower')
        # fig.colorbar(cax, ax=ax)
        ax.set_yticks(np.arange(len(unique_cats)))
        ax.set_yticklabels(unique_cats)
        ax.xaxis_date()

    if chart_type == 'scatter' or chart_type == 'line':
        _plot_scatter_or_line()
    elif chart_type == 'heatmap':
        _plot_heatmap()

    # Common plot settings
    ax.set_yticks(range(1, len(unique_cats) + 1))
    ax.set_yticklabels(unique_cats)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlabel(kwargs.get('xlabel', 'Date'))
    ax.set_title(kwargs.get('title', f'{chart_type.capitalize()} Chart'))

    if values is not None:
        # Handle numeric and ordinal values
        # Check if values are numeric; if not, try converting them
        if isinstance(values, list):
            values = pd.Series(values)
        if pd.api.types.is_numeric_dtype(values):
            # Create a colorbar if values are used for coloring
            sm = plt.cm.ScalarMappable(
                cmap=plt.cm.Greys,
                norm=plt.Normalize(vmin=values.min(), vmax=values.max()))
            sm._A = []  # Fake up the array of the scalar mappable.
            cbar = plt.colorbar(sm, ax=ax)
            cbar.set_label('Value Scale')
        elif isinstance(values.dtype, pd.CategoricalDtype):
            # Generate a legend based on the unique "values"
            unique_values = pd.Categorical(values).categories
            value_to_category_map = {
                val: categories[values.tolist().index(val)]
                for val in unique_values}
            handles = [
                plt.Line2D([0], [0],
                           color=category_colors[value_to_category_map[val]],
                           lw=4) for val in unique_values]

            # Convert unique_values to a list
            unique_values_list = unique_values.tolist()
            ax.legend(handles=handles, labels=unique_values_list,
                      title="Values", loc="best")
    elif kwargs.get('legend', False) and chart_type != 'heatmap':
        # Standard category legend
        ax.legend(title="Categories", loc="best")
    if ax is None:
        plt.tight_layout()
        plt.show()
        plt.close('all')


def _get_cat_cols(categories, values, kwargs):
    unique_cats = sorted(set(categories), key=categories.index)
    # Color and marker setup
    # gray_color_palette = plt.cm.Greys(
    #     np.linspace(0.2, 0.8, len(unique_cats)))
    # gray_color_palette = 'black'
    # Check for user-provided category colors in kwargs
    category_colors = kwargs.get('category_colors')

    if category_colors is None:
        if values is not None:
            # Handle numeric and ordinal values
            # Check if values are numeric; if not, try converting them
            if isinstance(values, list):
                values = pd.Series(values)
            if pd.api.types.is_numeric_dtype(values):
                if values.max() == values.min():
                    normalized_values = pd.Series([0.9] * len(values))
                else:
                    normalized_values = (values - values.min()) / (
                        values.max() - values.min())
            elif isinstance(values.dtype, pd.CategoricalDtype):
                # Attempt to convert to ordered categorical if it's not numeric
                try:
                    values = pd.Categorical(values, ordered=True)
                    numeric_values = values.codes
                    normalized_values = (
                        numeric_values - numeric_values.min()) / (
                            numeric_values.max() - numeric_values.min())
                except Exception as e:
                    print("Warning: failed to convert values to ordered " +
                          f"categorical. {str(e)}")
                    return  # Exit if conversion fails
            else:
                print("Warning: 'values' must be numeric or ordered " +
                      "categorical to use for color scaling. Defaulting to " +
                      "grayscale.")
                normalized_values = np.linspace(0.2, 0.8, len(categories))

            # Map normalized values to grayscale using categories as keys
            category_colors = {
                cat: plt.cm.Greys(0.2 + 0.6 * val) for cat,
                val in zip(categories, normalized_values)}
        else:
            # Default to uniform grayscale if no values are provided
            single_color = plt.cm.Greys(0.8)  # gray color
            category_colors = {cat: single_color for cat in unique_cats}
    else:
        # Use provided category colors if specified
        category_colors = {
            cat: color for cat, color in zip(unique_cats,
                                             category_colors)}

    return category_colors


def line(categories, start_dates, end_dates, values=None, markers=None,
         fig_kw={}, plot_kw={}, **kwargs):
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
    values : array-like, optional
        An optional array of numeric or ordered categorical values used to
        determine the color intensity or shade of the plot elements.
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
                  values=values, markers=markers, fig_kw=fig_kw,
                  plot_kw=plot_kw, **kwargs)
