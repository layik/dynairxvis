import matplotlib.pyplot as plt
from .time import grouped_chart
from .utils import FIG_SIZE


def plot_grid(categories_list, start_dates_list, end_dates_list,
              chart_types, values_list=None, fig_kw={}, **kwargs):
    """
    Plot multiple chart types in a grid layout with shared x-axis.

    Parameters
    ----------
    categories_list : list of list
        List of category arrays (one per chart).
    start_dates_list : list of list
        List of start dates arrays.
    end_dates_list : list of list
        List of end dates arrays.
    chart_types : list of str
        List of chart types ('line', 'scatter', 'gantt').
    values_list : list of arrays, optional
        List of value arrays for coloring.
    fig_kw : dict, optional
        Figure customization arguments.
    **kwargs : dict
        Additional arguments passed to individual charts.
    """
    n = len(chart_types)
    # Set default figure properties and apply scaling to height
    default_fig_kw = FIG_SIZE.copy()
    default_fig_kw['figsize'] = (FIG_SIZE['figsize'][0],
                                 FIG_SIZE['figsize'][1] * n)
    default_fig_kw.update(fig_kw)

    fig, axs = plt.subplots(n, 1, sharex=True, **default_fig_kw,
                            gridspec_kw={'hspace': 0.3})

    if n == 1:
        axs = [axs]  # Handle single plot case

    for i, (categories, start_dates, end_dates, chart_type) in enumerate(zip(
            categories_list, start_dates_list, end_dates_list, chart_types)):

        ax = axs[i]
        grouped_chart(categories, start_dates, end_dates,
                      chart_type=chart_type,
                      values=(values_list[i] if values_list else None),
                      ax=ax, fig_kw=fig_kw, **kwargs)

    plt.suptitle(kwargs.get('suptitle', 'Grouped Chart Grid'))
    plt.xlabel(kwargs.get('xlabel', 'Time'))
    plt.show()
