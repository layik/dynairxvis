import matplotlib.pyplot as plt


def pie(categories, values, fig_kw={}, **kwargs):
    """
    Creates and displays a grid of pie charts for given categories
    and associated values.

    Parameters
    ----------
    categories : list of str
        The categories for each pie chart.
    values : list of int or float
        The values associated with each category.
    fig_kw : dict, optional
        Keyword arguments for plt.subplots() to customize the figure.
    **kwargs : dict
        Additional keyword arguments for customization such as 'startangle',
        and 'colors'.

    Examples
    --------
    >>> categories = ['Category A', 'Category B', 'Category C']
    >>> values = [10, 20, 30]
    >>> pie(categories, values)
    """
    # Determine the number of pie charts based on categories
    num_pies = len(categories)

    # Set default figure properties
    default_fig_kw = {'figsize': (num_pies * 3, 3)}
    default_fig_kw.update(fig_kw)
    fig, axs = plt.subplots(1, num_pies, **default_fig_kw)

    # Ensure axs is iterable
    if num_pies == 1:
        axs = [axs]

    # DynAIRxVIS default gray color theme
    gray_color_palette = ['darkgray', 'lightgray']
    total = sum(values)
    # Loop through the categories and values, a pie chart for each
    for ax, category, value in zip(axs, categories, values):
        # Normalize value
        ax.pie([value/total, (total-value)/total], labels=[f'{value}', ''],
               colors=gray_color_palette, startangle=90,
               wedgeprops=dict(edgecolor='black'), normalize=True)
        ax.set_title(category)

    plt.tight_layout()
    plt.show()
