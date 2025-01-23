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
    violin_width, violin_height = (ax.get_position().width,
                                   ax.get_position().height)
    assert violin_height < violin_width, "Violin plot is not horizontal"

    plt.close(fig)  # Close the figure after test

@patch('matplotlib.pyplot.show')
def test_violin_dynamic_labels_and_title(mock_show):
    values = [1, 2, 3, 4, 5, 6, 7]
    violin(values, ylabel="Custom Y", xlabel="Custom X", title="Custom Title")
    fig = plt.gcf()
    ax = fig.axes[0]
    assert ax.get_ylabel() == "Custom Y", "Y-axis label not applied correctly"
    assert ax.get_xlabel() == "Custom X", "X-axis label not applied correctly"
    assert ax.get_title() == "Custom Title", "Title not applied correctly"
    plt.close(fig)

@patch('matplotlib.pyplot.show')
def test_violin_with_legend(mock_show):
    values = [1, 2, 3, 4, 5, 6, 7]
    violin(values, legend=True, legend_labels=["Test Legend"], legend_loc="upper right")
    fig = plt.gcf()
    ax = fig.axes[0]
    legend = ax.get_legend()
    assert legend is not None, "Legend not applied"
    assert legend.get_texts()[0].get_text() == "Test Legend", "Legend text incorrect"
    plt.close(fig)

@patch('matplotlib.pyplot.show')
def test_violin_grid_customization(mock_show):
    values = [1, 2, 3, 4, 5, 6, 7]
    violin(values, grid=True, grid_linestyle=":", grid_linewidth=0.8)
    fig = plt.gcf()
    ax = fig.axes[0]
    grid_lines = ax.yaxis.get_gridlines()  # For vertical plot
    assert len(grid_lines) > 0, "Grid lines not applied"
    assert grid_lines[0].get_linestyle() == ":", "Grid linestyle not applied correctly"
    assert grid_lines[0].get_linewidth() == 0.8, "Grid linewidth not applied correctly"
    plt.close(fig)
