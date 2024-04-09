from dynairxvis.plot import radar
import matplotlib.pyplot as plt
from unittest.mock import patch
import os


@patch('matplotlib.pyplot.show')
def test_radar_creates_plot(mock_show):
    # When radar calls plt.show(), it won't actually display the plot.
    # Instead, plt.show() does nothing during this test,
    # allowing the test to proceed without interruption.
    categories, values = ['N1', 'N2', 'N3'], [10, 15, 35]
    radar(categories, values)
    # Since plt.show() is mocked,
    # we can check the plot without it being cleared by plt.show().
    fig = plt.gcf()
    assert len(fig.axes) > 0, "No axes found in the plot"
    ax = fig.axes[0]  # Get the first (and in this case, only) axes object

    # Ensure the plot has 3 categories (N1, N2, N3)
    e = "Incorrect number of x-ticks"
    assert len(ax.get_xticks()) == len(categories), e

    # Check category labels
    e = "Category label is incorrect"
    assert ax.get_xticklabels()[0].get_text() == categories[0], e
    assert ax.get_xticklabels()[1].get_text() == categories[1], e
    assert ax.get_xticklabels()[2].get_text() == categories[2], e

    # Optionally, test if the plot has been saved to a file
    # This requires modifying the radar function to save the plot
    # filename = "test_plot.png"
    # radar(['N1', 'N2', 'N3'], [10, 15, 35], filename=filename)
    # assert os.path.isfile(filename), "Plot file was not created"
    # os.remove(filename)  # Clean up the file after test
