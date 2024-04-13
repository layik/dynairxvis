import matplotlib.pyplot as plt
import numpy as np
from .time import grouped_chart


def scatter(categories, start_dates=None, end_dates=None, values=None,
            mode='gantt', markers=None, fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a scatter plot with either custom markers for each
    category in a 'gantt'-like style or traditional scatter plot style with
    quantity on y-axis and nominal categories on x-axis based on mode.

    Parameters
    ----------
    categories : list of str
        The categories or names of the tasks or nominal categories on x-axis.
    values : list or list of lists
        If mode is 'gantt', these are end dates for each task.
        If mode is 'scatter', these are quantitative values for y-axis.
    mode : str, optional
        Determines the type of scatter plot. 'gantt' for gantt-like plot,
        'scatter' for traditional scatter plot. Default is 'gantt'.
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

    Example
    -------
    categories = ['Category A', 'Category B', 'Category C']
    values = [10, 20, 30] # For 'scatter' mode

    scatter(categories, values, mode='scatter')
    """
    if mode == 'gantt':
        if start_dates is None or end_dates is None:
            raise ValueError(
                "Start and end dates must be provided for 'gantt' mode.")
    elif mode == 'scatter':
        if values is None:
            raise ValueError(
                "Values must be provided for 'scatter' mode.")
    else:
        raise ValueError(
            "Invalid mode specified. Use 'gantt' or 'scatter'.")

    if mode == 'gantt':
        grouped_chart(categories, start_dates, end_dates,
                      chart_type='scatter', markers=markers,
                      fig_kw=fig_kw, plot_kw=plot_kw, **kwargs)
    elif mode == 'scatter':
        fig_kw = {**{'figsize': (6, 4)}, **fig_kw}
        fig, ax = plt.subplots(**fig_kw)

        color_theme = kwargs.get('color_theme',
                                 plt.cm.Greys(
                                     np.linspace(0.3, 0.9, len(categories))))
        # Ensure values are a flat list for traditional scatter plot mode
        if any(isinstance(val, list) for val in values):
            raise ValueError("Values must be a flat list when " +
                             "mode is 'scatter'.")

        # Map categories to x-axis indices
        x_indices = np.arange(len(categories))
        # Plot traditional scatter plot
        for i, value in enumerate(values):
            ax.scatter(x_indices[i], value, **plot_kw,
                       color=color_theme[i],
                       marker=markers.get(
                           categories[i], 'o') if markers else 'o')

        # Set category labels on x-axis
        ax.set_xticks(x_indices)
        ax.set_xticklabels(categories)
        # Set axis labels and title
        ax.set_ylabel(kwargs.get('ylabel', 'Quantity'))
        ax.set_xlabel(kwargs.get('xlabel', 'Categories'))
        ax.set_title(kwargs.get('title', 'Scatter Plot'))

        # Add additional customizations and show plot
        if 'xlim' in kwargs:
            ax.set_xlim(kwargs['xlim'])
        if 'ylim' in kwargs:
            ax.set_ylim(kwargs['ylim'])

        plt.tight_layout()
        plt.show()
