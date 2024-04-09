import matplotlib.pyplot as plt
import numpy as np


def radar(categories, values):
    """
    Creates and displays a radar chart based on
    the provided categories and values.

    Parameters
    ----------
    categories : list of str
        The categories to be plotted on the radar chart.
        Each category corresponds to one spoke on the radar chart.
    values : list of float
        The values for each category. Each value determines
        the distance from the center of the chart for
        its corresponding category.

    Returns
    -------
    None.

    Example
    -------
    categories = ['N1', 'N2', 'N3']
    values = [10, 15, 35]

    radar(categories, values)
    """
    # Number of variables we're plotting.
    num_vars = len(categories)

    # Compute angle each bar is centered on:
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The plot is circular, so we need to "complete the loop" and append the
    # start value to the end.
    values += values[:1]
    angles += angles[:1]

    # Plot
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='gray', alpha=0.25)
    ax.plot(angles, values, color='gray', linewidth=2)
    # Remove labels for the y-ticks
    ax.set_yticklabels([])
    # Set the category labels.
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Title
    plt.title('Radar Chart', y=1.1)

    plt.show()
