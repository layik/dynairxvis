import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import bar
from .test_utils import CATEGORIES, VALUES


@patch('matplotlib.pyplot.show')
def test_bar(mock_show):
    # Call the function without trying to unpack fig and ax
    bar(CATEGORIES, VALUES)

    # Obtain the current figure and axes
    fig = plt.gcf()
    ax = plt.gca()

    # Check if a figure and axis are created
    assert fig is not None, "No figure was created"
    assert ax is not None, "No axes were created"
    assert len(ax.containers) > 0, "No bars created in the plot"

    # Close the figure after the test
    plt.close(fig)
