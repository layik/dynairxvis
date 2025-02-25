import os
import matplotlib.pyplot as plt

from .dot import dot
from .box import box
from .bar import bar
from .pie import pie, table_list
from .time import line
from .gantt import gantt
# from .table import table
from .radar import radar
from .violin import violin
from .hist import histogram
from .scatter import scatter
from .heatmap import heatmap
from .calendar import calendar
from .utils import profile, findIndex

__all__ = ['calendar']

# For threshold of:  50.0 . These will be kept (10)
# 'Line', 'Table', 'Bar', 'List (Table)', 'Histogram', 'Dot',
# 'Gantt chart', 'Heatmap', 'Pie', 'Scatter'
# For threshold of:  50.0 . These will be ropped (4)
# 'Violin', 'Box', 'Radar', 'Donut'


# =============================================================================
# Internal
# =============================================================================
def _draw_fig(filename=None, overwrite=False, **kwargs):
    """
    Internal function, which is called to draw a plot to the screen or
    save it in a file.

    Parameters
    ----------
    filename : str, optional
        The filename for the figure. If None, the figure is displayed
        on the screen.
    overwrite : bool, optional
        If False, does not overwrite the file if it exists. If True,
        overwrites the file.
    **kwargs : dict
        Keyword arguments for fig.savefig().

    Returns
    -------
    None.
    """
    if filename is not None:
        if overwrite or not os.path.isfile(filename):
            fig = plt.gcf()
            fig.savefig(filename, **kwargs)
        else:
            print('** WARNING **: Figure not saved. File exists.')
            print(filename)
    else:
        plt.show()


# Mapping of plot_name to plotting function
# All 11 chart types added
plot_functions = {
    'bar': bar,
    'box': box,
    'dot': dot,
    'gantt': gantt,
    'line': line,
    'heatmap': heatmap,
    'hist': histogram,
    'pie': pie,
    'radar': radar,
    'scatter': scatter,
    'violin': violin
}


def plot(plot_name, *args, **kwargs):
    """
    High-level plotting function that dispatches to specific plotting functions
    based on plot_name. It then shows the plot or saves it to a file.

    Parameters
    ----------
    plot_name : str
        The name of the plot type to generate.
    *args : tuple
        Positional arguments passed directly to the plotting function.
    **kwargs : dict
        Keyword arguments passed directly to the plotting function. It should
        include 'filename' and 'overwrite' if saving the plot is desired.

    Returns
    -------
    None.
    """
    # Extract filename and overwrite from kwargs, defaulting to None and False
    # if not present
    filename = kwargs.pop('filename', None)
    overwrite = kwargs.pop('overwrite', False)

    if plot_name in plot_functions:
        # Create the plot
        plot_func = plot_functions[plot_name]
        # Ensure plot functions return fig, ax
        plot_func(*args, **kwargs)
    else:
        print(f"**WARNING: ** '{plot_name}' is not a supported plot type.")

    # Show the plot or save it to a file
    _draw_fig(filename=filename, overwrite=overwrite, **kwargs)


def plot_charts(df, column_refs=[], **kwargs):
    """
    Plots charts based on the provided column references (names or indices)
    and their data types.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame from which to plot data.
    column_refs : list
        List of column references (names or indices) to be used for plotting.
    **kwargs : dict
        Additional keyword arguments passed to plotting functions.

    Returns
    -------
    None

    Examples
    --------

    .. code-block:: python

        import pandas as pd
        from your_module_name import plot_charts

        # Sample DataFrame
        df = pd.DataFrame({
            'Blood_Pressure': [120, 130, 125, 118, 135],
            'Condition': ['Diabetes', 'Hypertension', 'Asthma',
                          'Cardiovascular', 'Obesity']
        })

        # Histogram of 'Blood_Pressure'
        plot_charts(df, column_refs=['Blood_Pressure'])

        # Bar chart with 'Condition' as categories & 'Blood_Pressure' as values
        plot_charts(df, column_refs=['Condition', 'Blood_Pressure'])

    """
    # Convert indices to column names if necessary
    col_names = [df.columns[idx] if isinstance(
        idx, int) else idx for idx in column_refs]

    # Basic validation
    if not col_names:
        raise ValueError("No column references provided for plotting.")

    col_types, col_codes, charts = profile(df[col_names],
                                           col_count=len(col_names))
    # TODO: Remove print statements
    print(col_codes, col_names)
    a = col_names.copy()
    a = [x.lower() for x in a]
    n_col = next((col for col, dtype in col_types.items() if dtype == 'N'),
                 None)
    o_col = next((col for col, dtype in col_types.items() if dtype == 'O'),
                 None)
    q_col = next((col for col, dtype in col_types.items() if dtype == 'Q'),
                 None)
    start = df[col_names[findIndex(a, 'start')]]
    end = df[col_names[findIndex(a, 'end')]]
    # Decision structure for plotting based on type codes and number of columns
    if len(col_names) == 1 and col_codes == 'Q':
        print(f"Q charts for {col_names[0]}...")
        histogram(df[col_names[0]], **kwargs)
        violin(df[col_names[0]], **kwargs)
        box(df[col_names[0]], **kwargs)
    elif len(col_names) == 1 and col_codes == 'N':
        print('N charts...')
        pie(df[col_names[0]], **kwargs)
        table_list(df[[col_names[0]]], **kwargs)
    elif (len(col_names) == 2 and col_codes == 'NQ'):
        print('NQ charts...')
        q_col = next(col for col,
                     dtype in col_types.items() if dtype == 'Q')
        # print(f"Plotting bar chart with categories from {n_col} and" +
        #       " values from {q_col}...")
        bar(df[n_col], df[q_col], **kwargs)
        scatter(df[n_col], values=df[q_col], mode='scatter')
        heatmap(df[n_col], values=df[q_col], mode='heatmap')
        pie(df[n_col], df[q_col])
    elif len(col_names) == 3 and col_codes == 'NTT':
        # NT
        print('NT charts...')
        gantt(df[n_col], start, end)
        pie(df[n_col], start_dates=start, end_dates=end, time=True)
        line(df[n_col], start_dates=start, end_dates=end)
        scatter(df[n_col], start_dates=start, end_dates=end, mode='gantt')
        heatmap(df[n_col], start_dates=start, end_dates=end, mode='gantt')
    elif len(col_names) == 4 and col_codes == 'NOTT':
        print('NTO charts...')
        _nott_nqtt(df[n_col], start, end, df[o_col])
        # ['Gantt', 'Line', 'Heatmap', 'Scatter']
    elif len(col_names) == 4 and col_codes == 'NQTT':
        print('NQT charts...')
        _nott_nqtt(df[n_col], start, end, df[q_col])
        # ['Gantt', 'Line', 'Heatmap', 'Scatter']
    else:
        print("No suitable plot type found for the columns or data types.")


def _nott_nqtt(categories, starts, ends, values):
    """
    Utility function to plot Gantt, Line, Heatmap, and Scatter plots for
    combinations of categories, start dates, end dates, and values. This
    can be combination of nominal, ordinal, two temporal columns of data or
    nominal, quantitative, and two columns of temporal data.

    Parameters
    ----------
    categories : list of str
        The categories or names for the tasks or events.
    starts : list of datetime
        The start dates for each task or event.
    ends : list of datetime
        The end dates for each task or event.
    values : list of numeric or str, optional
        The values associated with each category. These can be used to adjust
        bar heights, line colors, or other plot characteristics.

    Raises
    ------
    ValueError
        If the input lists (categories, starts, ends, values) do not have the
        same length.

    Examples
    --------
    >>> categories = ['Task A', 'Task B', 'Task C']
    >>> starts = [datetime(2020, 1, 1), datetime(2020, 6, 1),
        datetime(2020, 8, 1)]
    >>> ends = [datetime(2021, 1, 1), datetime(2020, 7, 1),
        datetime(2020, 9, 1)]
    >>> values = [2, 4, 6]
    >>> _nott_nqtt(categories, starts, ends, values)
    """
    # Input validation
    if not (len(categories) == len(starts) == len(ends) == len(values)):
        raise ValueError("All input lists must have the same length to \
            generate Gantt, Line, Heatmap, and Scatter plots.")

    # Plot Gantt chart
    gantt(categories, starts, ends, values)

    # Plot Line chart
    line(categories, start_dates=starts, end_dates=ends, values=values)

    # Plot Heatmap
    heatmap(categories=categories, start_dates=starts, end_dates=ends,
            values=values, mode='gantt')

    # Plot Scatter plot
    scatter(categories, start_dates=starts, end_dates=ends, values=values,
            mode='gantt')
