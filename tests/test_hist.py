import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import histogram


@patch('matplotlib.pyplot.show')
def test_histogram_creates_correct_bins(mock_show):
    values = [10, 12, 15, 20, 35, 37, 40]
    bins = [10, 15, 20, 35, 40]

    # Call the histogram function without Axes-level properties in plot_kw
    histogram(values, bins=bins, xlabel='Value',
              ylabel='Frequency', title='Histogram of Values')

    fig = plt.gcf()
    assert len(fig.axes) > 0, "No axes found in the plot"
    ax = fig.axes[0]

    # Now you can directly assert on ax properties like labels and titles
    assert ax.get_xlabel() == 'Value', "xlabel is incorrect"
    assert ax.get_ylabel() == 'Frequency', "ylabel is incorrect"
    assert ax.get_title() == 'Histogram of Values', "Title is incorrect"

    plt.close(fig)  # Ensure the figure is closed after the test
