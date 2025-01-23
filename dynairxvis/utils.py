import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt


FIG_SIZE = {'figsize': (6, 4)}
NOQT = ['Gantt', 'Line', 'Heatmap', 'Scatter']
DT_CHARTS = {"Q": ['Histogram'],
             "N": ['List (Table)', 'Pie'],
             "NQ": ['Bar', 'Scatter', 'Heatmap', 'Table', 'Pie'],
             "NT": ['Gantt', 'Pie', 'Line', 'Scatter', 'Heatmap'],
             "NOT": NOQT,
             "NQT": NOQT
             }


def _infer_data_type(column):
    # Temporal: check if the column is datetime
    if pd.api.types.is_datetime64_any_dtype(column):
        return 'T'  # Temporal

    # Quantitative: numeric data that is not categorically divided
    if column.dtype.kind in 'iuf':
        if column.nunique() / len(column) > 0.1:  # Arbitrary threshold
            return 'Q'  # Quantitative

    # Ordinal: ordered categories or numeric with few unique values
    if isinstance(column.dtype, pd.CategoricalDtype) and column.cat.ordered:
        return 'O'  # Potentially ordinal
    # Small number of unique values
    elif column.dtype.kind in 'iuf' and column.nunique() <= 10:
        return 'O'  # Potentially ordinal

    # Nominal: everything else
    return 'N'  # Nominal


def _apply_inference(df):
    return {col: _infer_data_type(df[col]) for col in df.columns}


def profile(df, col_count=3):
    """
    Determines appropriate chart types based on the DataFrame's
    column data types and count. This function infers data types for the first
    few columns of the DataFrame and suggests suitable chart types based on
    these types.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame for which to infer chart types.
    col_count : int, optional
        The number of columns to consider for the type inference. Default is 3.

    Returns:
    -------
    tuple
        - A dictionary mapping the first three (or fewer) DataFrame columns to
        their inferred data types (encoded as 'N', 'O', 'Q', 'T' for nominal,
        ordinal, quantitative, and temporal types respectively).
        - A string representing the combined codes of the inferred data types.
        - A list of suggested chart types based on the inferred data types.

    Raises:
    -------
    ValueError
        If the DataFrame is empty or has fewer columns than `col_count`.
    """
    if df.empty:
        raise ValueError("The provided DataFrame is empty.")
    if len(df.columns) < col_count:
        raise ValueError(
            f"The DataFrame must have at least {col_count} columns.")

    try:
        # Infer data types for the specified number of columns
        col_types = _apply_inference(df.iloc[:, :col_count])
        col_codes = ''.join(sorted(col_types.values()))
        suggested_charts = DT_CHARTS.get(col_codes,
                                         ['No appropriate chart found'])
        return col_types, col_codes, suggested_charts
    except Exception as e:
        raise RuntimeError(f"Failed to profile the DataFrame: {str(e)}")


def findIndex(a, str):
    indices = [idx for idx, s in enumerate(a) if str in s]
    return indices[0] if indices else 0


def is_valid_array(input_array):
    """
    Checks if the provided input is an array-like object and is not empty.

    Parameters:
    input_array : list, np.ndarray, pd.Series
        The input to check for array-like and non-empty properties.

    Returns:
    bool
        True if the input is array-like and non-empty, False otherwise.
    """
    return isinstance(
        input_array, (list, np.ndarray, pd.Series)) and len(input_array) > 0


def get_color_palette(n_colors):
    """
    Generate a grayscale color palette with n distinct colors.
    """
    return [cm.Greys(i / n_colors) for i in range(n_colors)]


def _plot_now_line(ax, max_date=None, label='Now'):
    """
    Plot a vertical line at the current datetime if within 1 year from the max
    x-axis limit.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to plot the "now" line on.
    max_date : datetime, optional
        The maximum date to consider for plotting the "now" line.
        If not provided, it will be inferred from the axis limits.
    label : str, optional default 'Now'
    """
    if not isinstance(ax, plt.Axes):
        raise TypeError("ax must be a matplotlib.axes.Axes instance")

    now = datetime.now()

    if max_date is None:
        xlims = ax.get_xlim()
        max_date = mdates.num2date(xlims[1])
    elif not isinstance(max_date, datetime):
        raise TypeError("max_date must be a datetime instance")

    # Make 'now' timezone-aware to match 'max_date'
    if (max_date.tzinfo is not None and
            max_date.tzinfo.utcoffset(max_date) is not None):
        now = now.astimezone(max_date.tzinfo)
    # TODO: in future make the year scale of the x-axis a package wide setting
    # then the following code can be amended to use that setting
    # Plot "now" vertical line if within 1 year from max xlim
    if (max_date - now).days <= 365:
        ax.axvline(mdates.date2num(now), color='red', linestyle='--',
                   linewidth=1)
        ax.annotate(label, (mdates.date2num(now), ax.get_ylim()[1] * 0.95),
                    xytext=(10, 0), textcoords='offset points', color='red')
    if not isinstance(ax, plt.Axes):
        raise TypeError("ax must be a matplotlib.axes.Axes instance")


def _resolve_orientation(orientation):
    """
    Resolves orientation strings flexibly based on substrings.

    Parameters
    ----------
    orientation : str
        The orientation string to resolve. Valid inputs include:
        - Any substring containing 'vert' resolves to 'vertical'.
        - Any substring containing 'hori' resolves to 'horizontal'.

    Returns
    -------
    str
        The resolved full-length orientation string
        ('vertical' or 'horizontal').

    Raises
    ------
    ValueError
        If the input string cannot be resolved to a valid orientation.
    """
    orientation_lower = orientation.lower()
    if "vert" in orientation_lower:
        return "vertical"
    elif "hori" in orientation_lower:
        return "horizontal"
    else:
        raise ValueError(
            f"Invalid orientation: '{orientation}'. "
            "Expected 'vertical' or 'horizontal' "
            "(or substrings like 'vert', 'hori')."
        )
