import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import box


@patch('matplotlib.pyplot.show')
def test_box_creates_plot(mock_show):
    values = [1, 2, 2, 3, 4, 4, 4, 5, 6, 7]

    # Test the vertical box plot
    box(values)
    fig = plt.gcf()
    ax = fig.axes[0]
    assert len(ax.lines) > 0, "No lines found in the plot (vertical)"

    plt.close(fig)  # Close the figure before the next test

    # Test the horizontal box plot
    box(values, horizontal=True)
    fig = plt.gcf()
    ax = fig.axes[0]
    # Check if the plot is horizontal by comparing width and height
    box_width, box_height = ax.get_position().width, ax.get_position().height
    assert box_height < box_width, "Box plot is not horizontal"

    plt.close(fig)  # Close the figure after test
