import matplotlib.pyplot as plt
from .time import grouped_chart
from .utils import FIG_SIZE
from .gantt import gantt


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
        List of chart types ('line', 'scatter', 'heatmap', 'gantt').
    values_list : list of arrays, optional
        List of value arrays for coloring.
    fig_kw : dict, optional
        Figure customization arguments.
    **kwargs : dict
        Additional arguments passed to individual charts.
    """
    # TODO: input validation
    # validate chart types, for now just line, scatter and heatmap
    for chart_type in chart_types:
        if chart_type.lower() not in ['line', 'scatter', 'heatmap', 'gantt']:
            print(f"Error: Invalid chart type '{chart_type}'. "
                  "Choose from 'line', 'scatter', 'heatmap' or 'gantt'.")
            return

    # Determine the minimum length across lists
    lengths = [len(categories_list), len(start_dates_list),
               len(end_dates_list), len(chart_types)]
    min_length = min(lengths)

    # Handle the values_list if provided
    if values_list:
        lengths.append(len(values_list))
        min_length = min(min_length, len(values_list))

    # Early exit if there are no charts to plot
    if min_length == 0 or len(chart_types) == 0:
        print("**Warning:** Either a list is missing or empty. Or "
              "no chart types provided. Nothing to plot.")
        return

    # Print warning if the lists have different lengths
    if len(set(lengths)) > 1:
        chart_word = "chart" if min_length == 1 else "charts"
        print("**Warning:** Mismatch detected. "
              f"Plotting first {min_length} {chart_word}.")

    # Truncate all lists to the shortest length
    categories_list = categories_list[:min_length]
    start_dates_list = start_dates_list[:min_length]
    end_dates_list = end_dates_list[:min_length]
    chart_types = chart_types[:min_length]
    if values_list:
        values_list = values_list[:min_length]

    # Set default figure properties and apply scaling to height
    n = len(chart_types)
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
        if chart_type.lower() == 'gantt':
            gantt(categories, start_dates, end_dates,
                  values=(values_list[i] if values_list else None),
                  ax=ax, fig_kw=fig_kw, **kwargs)
        else:
            grouped_chart(categories, start_dates, end_dates,
                          chart_type=chart_type,
                          values=(values_list[i] if values_list else None),
                          ax=ax, fig_kw=fig_kw, **kwargs)

    plt.suptitle(kwargs.get('suptitle', 'Chart Grid'))
    plt.show()
