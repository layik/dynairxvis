import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def scatter(categories, start_dates, end_dates, markers, fig_kw={},
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
    markers : dict
        A dictionary mapping categories to marker styles.
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
    default_fig_kw = {'figsize': (6, 4)}
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    # Calculate category_positions based on unique_categories
    unique_categories = sorted(set(categories), key=categories.index)
    category_positions = {category: pos for pos,
                          category in enumerate(unique_categories, start=1)}

    for start_date, end_date, category in zip(start_dates,
                                              end_dates, categories):
        y_position = category_positions[category]
        # Use custom marker or default to 'o'
        marker = markers.get(category, 'o')
        ax.scatter([start_date, end_date], [y_position, y_position],
                   marker=marker, **plot_kw)

    # Adjust y-axis to show category labels
    plt.yticks(list(category_positions.values()), unique_categories)

    ax.xaxis_date()
    myFmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_formatter(myFmt)

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel(kwargs.get('xlabel', 'Time'))
    plt.title(kwargs.get('title', 'Grouped Scatter Chart with Custom Markers'))
    plt.tight_layout()
    plt.show()
