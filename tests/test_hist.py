import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import histogram


@patch('matplotlib.pyplot.show')
def test_histogram_creates_correct_bins(mock_show):
    values = [10, 12, 15, 20, 35, 37, 40]
    bins = [10, 15, 20, 35, 40]

    # Default vertical histogram
    histogram(values, bins=bins, xlabel='Value', ylabel='Frequency',
              title='Histogram of Values')
    fig = plt.gcf()
    ax = fig.axes[0]
    assert len(fig.axes) > 0, "No axes found in the plot"
    assert ax.get_xlabel() == 'Value', "xlabel is incorrect"
    assert ax.get_ylabel() == 'Frequency', "ylabel is incorrect"
    assert ax.get_title() == 'Histogram of Values', "Title is incorrect"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_histogram_horizontal_orientation(mock_show):
    values = [10, 12, 15, 20, 35, 37, 40]
    bins = [10, 15, 20, 35, 40]

    # Horizontal histogram
    histogram(
        values,
        bins=bins,
        orientation='horizontal',
        xlabel='Frequency',
        ylabel='Value',
        title='Horizontal Histogram')
    fig = plt.gcf()
    ax = fig.axes[0]
    assert ax.get_ylabel() == 'Value', (
        "ylabel is incorrect for horizontal orientation")
    assert ax.get_xlabel() == 'Frequency', (
        "xlabel is incorrect for horizontal orientation")
    assert ax.get_title() == 'Horizontal Histogram', (
        "Title is incorrect for horizontal orientation")
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_histogram_custom_ticks(mock_show):
    values = [10, 12, 15, 20, 35, 37, 40]
    bins = [10, 15, 20, 35, 40]

    # Custom ticks
    xticks = [10, 20, 40]
    xticklabels = ['Low', 'Medium', 'High']
    histogram(values, bins=bins, xticks=xticks, xticklabels=xticklabels)
    fig = plt.gcf()
    ax = fig.axes[0]
    assert ax.get_xticks().tolist() == xticks, "xticks are incorrect"
    assert [tick.get_text() for tick in ax.get_xticklabels()] == xticklabels, (
        "xticklabels are incorrect")
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_histogram_custom_fig_kw(mock_show):
    values = [10, 12, 15, 20, 35, 37, 40]
    bins = [10, 15, 20, 35, 40]

    # Custom figure size
    histogram(values, bins=bins, fig_kw={'figsize': (8, 6)})
    fig = plt.gcf()
    assert fig.get_size_inches().tolist() == [8, 6], "Figure size is incorrect"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_histogram_custom_plot_kw(mock_show):
    values = [10, 12, 15, 20, 35, 37, 40]
    bins = [10, 15, 20, 35, 40]

    # Custom plot properties
    histogram(values, bins=bins, plot_kw={'color': 'red', 'alpha': 0.7})
    fig = plt.gcf()
    ax = fig.axes[0]
    for bar in ax.patches:
        assert bar.get_facecolor() == (1.0, 0.0, 0.0, 0.7), (
            "Plot color or alpha is incorrect")
    plt.close(fig)
