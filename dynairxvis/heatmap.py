import numpy as np
import matplotlib.pyplot as plt


def heatmap(categories, values, fig_kw={}, cmap='Greys', **kwargs):
    """
    Creates and displays a heatmap for given categories and associated values.

    Parameters
    ----------
    categories : list of str
        The categories for the y-axis of the heatmap.
    values : list of int or float, as flat or nested list.
        The values associated with each category.
    fig_kw : dict, optional
        Keyword arguments for plt.subplots() to customize the figure.
    cmap : str or Colormap, optional
        The colormap to use for the heatmap.
    **kwargs : dict
        Additional keyword arguments for customization such as 'xlabel',
        'ylabel', and 'title'.

    Examples
    --------
    >>> categories = ['Category 1', 'Category 2', 'Category 3']
    >>> values = [1, 2, 3]
    >>> heatmap(categories, values)
    """
    # Improved flattening function that checks type of each item
    def flatten(values):
        flattened_values = []
        for item in values:
            if isinstance(item, list):
                flattened_values.extend(item)
            else:
                flattened_values.append(item)
        return flattened_values

    # Determine if values are nested and find unique values
    flattened_values = flatten(values)
    unique_values = sorted(set(flattened_values))
    heatmap_matrix = np.zeros((len(categories), len(unique_values)))

    # Fill the heatmap matrix
    for i, item in enumerate(values):
        if not isinstance(item, list):
            item = [item]  # Treat single values as list
        for value in item:
            value_index = unique_values.index(value)
            heatmap_matrix[i, value_index] += 1  # Increment for occurrences

    # Set default figure properties
    default_fig_kw = {'figsize': (5, len(categories))}
    default_fig_kw.update(fig_kw)
    fig, ax = plt.subplots(**default_fig_kw)

    # Create the heatmap
    cax = ax.matshow(heatmap_matrix, cmap=cmap, aspect='auto')

    # Set ticks and labels
    ax.set_xticks(np.arange(len(unique_values)))
    ax.set_xticklabels(unique_values)
    ax.set_yticks(np.arange(len(categories)))
    ax.set_yticklabels(categories)

    # Move x-ticks to the top if preferred
    if kwargs.get('xticks_top', False):
        ax.xaxis.set_ticks_position('top')

    # Set axis labels and title
    ax.set_ylabel(kwargs.get('ylabel', 'Categories'))
    ax.set_title(kwargs.get('title', 'Heatmap'))

    # Colorbar settings if needed
    if kwargs.get('colorbar', False):
        fig.colorbar(cax, ax=ax, orientation='vertical')

    # Additional plot adjustments
    plt.tight_layout()
    plt.show()
