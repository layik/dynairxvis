import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import radar
from .test_utils import CATEGORIES, VALUES


@patch('matplotlib.pyplot.show')
def test_radar_creates_plot(mock_show):
    # When radar calls plt.show(), it won't actually display the plot.
    # Instead, plt.show() does nothing during this test,
    # allowing the test to proceed without interruption.
    radar(CATEGORIES, VALUES)
    # Since plt.show() is mocked,
    # we can check the plot without it being cleared by plt.show().
    fig = plt.gcf()
    assert len(fig.axes) > 0, "No axes found in the plot"
    ax = fig.axes[0]  # Get the first (and in this case, only) axes object

    # Ensure the plot has 3 CATEGORIES (N1, N2, N3)
    e = "Incorrect number of x-ticks"
    assert len(ax.get_xticks()) == len(CATEGORIES), e

    # Check category labels
    e = "Category label is incorrect"
    assert ax.get_xticklabels()[0].get_text() == CATEGORIES[0], e
    assert ax.get_xticklabels()[1].get_text() == CATEGORIES[1], e
    assert ax.get_xticklabels()[2].get_text() == CATEGORIES[2], e
