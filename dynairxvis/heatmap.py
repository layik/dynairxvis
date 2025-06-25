from .time import grouped_chart
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import colorsys

xfs = 11
yfs = 11
chart_h = 6
chart_w = 12
dpi = 100


def add_colorbar(ax, cmap, vmin, vmax, label="Event Count",
                 font_size=xfs):
    """
    Adds a color legend (colorbars) to a heatmap
    Panametens :
    etc
    """
    # mappable object for cbar
    norm = Normalize(vmin=vmin, vmax=vmax)
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # density hence

    cbar = plt.colorbar(sm, ax=ax, orientation='horizontal',
                        location='top',
                        ticks=range(vmin, vmax + 1),
                        fraction=0.05, pad=0.02)
    cbar.ax.tick_params(labelsize=font_size)
    cbar.set_label(label, fontsize=font_size)


def color_contrast(rgba, thresh=0.5):
    r, g, b, _ = rgba
    _, lightness, _ = colorsys.rgb_to_hls(r, g, b)
    return 'black' if lightness > thresh else 'white'


def heatmap(adf, date_col='obsdate', y_col='Disease',
            fig_kw={}, **kwargs):
    """
    Creates a heatmap of disease counts over years. It also takes
    additional parameters to customize the appearance of the heatmap.

    Parameters
    ----------
    adf : pd.DataFrame
        DataFrame containing the data to be visualized.
    date_col : str
        The name of the column containing date information.
    y_col : str
        The name of the column containing disease names.
    fig_kw : dict
        Additional keyword arguments for customizing the figure size and 
        layout.
    **kwargs : dict
        Additional keyword arguments for customizing the heatmap, such as:
        - 'font_size': Font size for the x and y axis labels.
        - 'title': Title of the heatmap.
    Example
    -------
    >>> heatmap(adf, date_col='obsdate', y_col='Disease',
            fig_kw={'figsize': (12, 6)},
            font_size=12, title='Disease Heatmap')
    >>> adf = pd.DataFrame({
            'obsdate': pd.date_range(start='2020-01-01',
            end='2021-01-01', freq='M'),
            'Disease': ['Disease A', 'Disease B'] * 13
        })
    >>> heatmap(adf, date_col='obsdate', y_col='Disease',
            fig_kw={'figsize': (12, 6)},
            font_size=12, title='Disease Heatmap')
    """
    assert isinstance(adf, pd.DataFrame)
    adf['year'] = adf[date_col].dt.year
    min_year, max_year = adf['year'].min(), adf['year'].max()
    year_bins = range(min_year, max_year + 1)

    data = (
        adf.groupby([y_col, 'year'], sort=False)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=year_bins, fill_value=0)
    )
    default_figsize = {'figsize': (chart_w, chart_h)}
    default_figsize.update(fig_kw)
    fig, ax = plt.subplots(**default_figsize)
    # fonts
    x_fs = kwargs.get("font_size", xfs)
    y_fs = kwargs.get("font_size", yfs)

    diseases = data.index
    years = data.columns

    for i, disease, in enumerate(diseases):
        for j, year in enumerate(years):
            count = data.at[disease, year]
            color = plt.cm.Greys(count/data.values.max())
            ax.add_patch(
                plt.Rectangle(
                    (j, i), 1, 1,
                    color=color,
                    ec='black'
                )
            )
            if count > 0:
                ax.text(
                    j + 0.5, 1 + 0.5, str(count),
                    ha='center', va='center', fontsize=x_fs,
                    color=color_contrast(color)
                )
                # add a scatter marker?
                # ax. scatter(j + 0.5, i + 0.5,
                #   color='black', s=10, alpha=0.2)

    # ax tick font sizes
    ax.set_xticks(np.arange(len(years)) + 0.5)
    ax.set_xticklabels(years, rotation=45, fontsize=x_fs)
    ax.set_yticks(np.arange(len(diseases)) + 0.5)
    ax.set_yticklabels(diseases, fontsize=y_fs)
    ax.set_xlim(0, len(years))
    ax.set_ylim(0, len(diseases))
    # ax.set_ylabel('Diseases')
    ax.grid(False)

    add_colorbar(ax, plt.cm.Greys, vmin=0, vmax=data.values.max(),
                 font_size=x_fs)
    plt.tight_layout()
    plt.title(kwargs.get('title', 'Heatmap'), fontsize=x_fs+1)
    plt.show()


def heatmap_nq(categories, values=None, start_dates=None, end_dates=None,
               ax=None, mode='heatmap', fig_kw={}, cmap='Greys', **kwargs):
    """
    Creates and displays a heatmap for given categories
    and associated values or time intervals.

    Parameters
    ----------
    categories : list of str
        The categories for the y-axis of the heatmap.
    values : list of int or float, as flat or nested list (for 'heatmap' mode).
        The values associated with each category.
    start_dates, end_dates : list of datetime (for 'gantt' mode)
        Start and end dates for each category interval.
    mode : str, optional
        'heatmap' for a standard value-based heatmap,
        'gantt' for a time-interval based heatmap.
    ax : matplotlib.axes.Axes, optional
        Axes object to plot on. If None, creates a new figure and axis.
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
    >>> heatmap(categories, values=values, mode='heatmap')
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

    # Aggregate values by category
    category_values = defaultdict(list)
    for cat, val in zip(categories, values):
        if isinstance(val, list):
            category_values[cat].extend(val)
        else:
            category_values[cat].append(val)

    unique_categories = sorted(category_values.keys())
    unique_values = sorted(set(flatten(values)))
    heatmap_matrix = np.zeros((len(unique_categories), len(unique_values)))

    # Fill the heatmap matrix
    for i, cat in enumerate(unique_categories):
        for val in category_values[cat]:
            value_index = unique_values.index(val)
            heatmap_matrix[i, value_index] += 1  # Increment for occurrences

    # Set default figure properties
    default_fig_kw = {'figsize': (5, len(unique_categories))}
    default_fig_kw.update(fig_kw)
    # Use existing ax or create new figure and axis
    if ax is None:
        fig, ax = plt.subplots(**default_fig_kw)

    # Create the heatmap
    cax = ax.matshow(heatmap_matrix, cmap=cmap, aspect='auto')

    # Set ticks and labels
    ax.set_xticks(np.arange(len(unique_values)))
    ax.set_xticklabels(unique_values, rotation=45, ha='left')
    ax.set_yticks(np.arange(len(unique_categories)))
    ax.set_yticklabels(unique_categories)

    # Move x-ticks to the top if preferred
    if kwargs.get('xticks_top', False):
        ax.xaxis.set_ticks_position('top')

    # Set axis labels and title
    ax.set_xlabel(kwargs.get('xlabel', 'Values'))
    ax.set_ylabel(kwargs.get('ylabel', 'Categories'))
    ax.set_title(kwargs.get('title', 'Heatmap'))

    # Colorbar settings if needed
    if kwargs.get('colorbar', False):
        if ax is None:
            fig.colorbar(cax, ax=ax, **kwargs.get('colorbar_kw', {}))
        else:
            ax.figure.colorbar(cax, ax=ax, **kwargs.get('colorbar_kw', {}))

    # Additional plot adjustments
    if ax is None:
        plt.tight_layout()
        plt.show()
