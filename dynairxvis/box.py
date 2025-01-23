import matplotlib.pyplot as plt
from .utils import FIG_SIZE

def box(values, horizontal=False, fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a box plot based on the provided values.

    Parameters
    ----------
    values : list of float
        The values to be included in the box plot.
    horizontal : bool, optional
        Whether to display the box plot horizontally. Defaults to False.
    fig_kw : dict
        Keyword arguments for plt.figure() to customize the figure.
    plot_kw : dict
        Keyword arguments for plt.boxplot() for further customization.
    **kwargs : dict
        Additional keyword arguments for customization.

    Example
    -------
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    box(values)
    """
    # Setup default figure size
    default_fig_kw = FIG_SIZE.copy()
    default_fig_kw.update(fig_kw)

    # Create the figure
    plt.figure(**default_fig_kw)

    # Configure median properties if not provided
    medianprops = plot_kw.pop('medianprops', {'color': 'black', 'linewidth': 2})

    # Plot the box plot
    plt.boxplot(
        values,
        orientation='horizontal' if horizontal else 'vertical',
        medianprops=medianprops,
        **plot_kw
    )

    # Set axis labels and grid
    if horizontal:
        plt.xlabel(kwargs.get('xlabel', 'Values'))  # Set xlabel
        plt.yticks([1], kwargs.get('yticks_labels', ['Value Set']))
        plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    else:
        plt.ylabel(kwargs.get('ylabel', 'Values'))  # Set ylabel
        plt.xticks([1], kwargs.get('xticks_labels', ['Value Set']))
        plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)

    # Apply title
    plt.title(kwargs.get('title', 'Box Plot of Values'))

    # Show the plot
    plt.show()
