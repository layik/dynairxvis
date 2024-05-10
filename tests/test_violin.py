import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import violin


@patch('matplotlib.pyplot.show')
def test_violin_creates_plot(mock_show):
    values = [1, 2, 2, 3, 4, 4, 4, 5, 6, 7]

    # Test the vertical violin plot
    violin(values)
    fig = plt.gcf()
    ax = fig.axes[0]
    m = "No collections found in the plot (vertical)"
    assert len(ax.collections) > 0, m

    plt.close(fig)  # Close the figure before the next test

    # Test the horizontal violin plot
    violin(values, horizontal=True)
    fig = plt.gcf()
    ax = fig.axes[0]
    # Check if the plot is horizontal by comparing width and height
    violin_width, violin_height = ax.get_position().width, ax.get_position().height
    assert violin_height < violin_width, "Violin plot is not horizontal"

    plt.close(fig)  # Close the figure after test
