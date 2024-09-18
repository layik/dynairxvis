import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import pandas as pd

from .utils import FIG_SIZE, get_color_palette


def gantt(categories, start_dates, end_dates, values=None,
          use_values_as_height=False, fig_kw={}, plot_kw={}, **kwargs):
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
    values : list of numeric or str, optional
        The values for each bar in the Gantt chart. If numeric, these values
        will be used to adjust the bar height dynamically or as hue for colors.
    use_values_as_height : bool, optional
        Whether to use the values to adjust the bar height. Default is False,
        which uses values as hue for coloring.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
    plot_kw : dict
        Keyword arguments for ax.barh() to further customize the bars.
    **kwargs : dict
        Additional keyword arguments for customization not related to ax.barh().
        This includes 'xlabel', 'title', and any axis formatter settings.

    Example
    -------
    gantt(categories=['Task A', 'Task B', 'Task C'],
          start_dates=[datetime(2020, 1, 1), datetime(2020, 6, 1)],
          end_dates=[datetime(2021, 1, 1), datetime(2020, 7, 1)],
          values=[2, 3, 5], use_values_as_height=True)
    """
    # Set up default figure settings
    default_fig_kw = FIG_SIZE
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)
    SINGLE_COLOR = 'gray'

    # If values is not provided, generate a color map based on the unique
    # categories
    if values is None:
        unique_cats = list(set(categories))
        single_color = plt.cm.Greys(0.8)  # Gray color
        unique_colors = {cat: single_color for cat in unique_cats}
    else:
        if pd.api.types.is_numeric_dtype(pd.Series(values)):
            if use_values_as_height:
                # Scale values for height
                max_height = max(values)
                min_height = min(values)

                def height_scaling(x): return 0.1 + 0.3 * (x - min_height) / \
                    (max_height - min_height) if max_height != min_height \
                    else 0.4
                unique_colors = {cat: SINGLE_COLOR for cat in categories}
            else:
                # Use values as hue for colors
                unique_cats = list(set(values))
                unique_colors = {
                    val: plt.cm.Greys(0.2 + 0.6 * (
                        val - min(values)) / (
                            max(values) - min(values))) for val in unique_cats}
        else:
            unique_cats = list(set(values))
            unique_colors = dict(zip(unique_cats,
                                     get_color_palette(len(unique_cats))))

    # Track which categories have been added to the legend
    legend_patches = {}

    # Plot each task using the provided plot kwargs
    for i, (category, start, end) in enumerate(zip(categories, start_dates,
                                                   end_dates)):
        if (values is not None
            and pd.api.types.is_numeric_dtype(pd.Series(values))
                and use_values_as_height):
            height = height_scaling(values[i])
        else:
            height = 0.4

        # Determine the color based on the logic
        if values is not None and not use_values_as_height:
            color_key = values[i]
        else:
            color_key = category

        color = unique_colors.get(color_key, 'black')
        ax.barh(category, end - start, left=start, height=height, color=color,
                edgecolor='black', **plot_kw)

        # Only add unique color keys to the legend
        if values is not None and not use_values_as_height:
            if color_key not in legend_patches:
                legend_patches[color_key] = Patch(facecolor=color,
                                                  edgecolor='black',
                                                  label=color_key)

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

    # Add labels, and title using kwargs
    plt.xlabel(kwargs.get('xlabel', 'Time'))
    plt.title(kwargs.get('title', 'Gantt Chart'))

    # Add legend if values are provided and used as height
    if values is not None:
        if use_values_as_height:
            height_values = [height for height in sorted(set(values))]
            height_labels = [f'{v:.2f}' for v in height_values]
            # Create custom legend elements with varying linewidths to represent heights
            legend_handles = [
                plt.Line2D([0], [0], color=SINGLE_COLOR,
                           lw=height_scaling(val) * 20, label=label)
                for val, label in zip(height_values, height_labels)
            ]

            # Add the custom lines to the legend
            plt.legend(handles=legend_handles, title='Bar Heights', loc='best')
        else:
            plt.legend(handles=list(legend_patches.values()), title='Values')

    plt.tight_layout()
    plt.show()
