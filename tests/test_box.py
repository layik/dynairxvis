import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import box


@patch('matplotlib.pyplot.show')
def test_box_creates_plot(mock_show):
    values = [1, 2, 2, 3, 4, 4, 4, 5, 6, 7]

    # Test the vertical box plot
    box(values, title="Vertical Box Plot", ylabel="Values",
        xticks_labels=["Test Set"])
    fig = plt.gcf()
    ax = fig.axes[0]
    assert len(ax.lines) > 0, "No lines found in the plot (vertical)"
    assert ax.get_ylabel() == "Values", "Y-axis label not applied correctly"
    assert ax.get_xticklabels()[0].get_text() == "Test Set", (
        "X-tick label not applied correctly"
    )
    assert ax.get_title() == "Vertical Box Plot", "Title not applied correctly"

    plt.close(fig)  # Close the figure before the next test

    # Test the horizontal box plot
    box(values, horizontal=True, title="Horizontal Box Plot", xlabel="Values",
        yticks_labels=["Test Set"])
    fig = plt.gcf()
    ax = fig.axes[0]
    assert len(ax.lines) > 0, "No lines found in the plot (horizontal)"
    assert ax.get_xlabel() == "Values", "X-axis label not applied correctly"
    assert ax.get_yticklabels()[0].get_text() == "Test Set", (
        "Y-tick label not applied correctly"
    )
    assert ax.get_title() == "Horizontal Box Plot", (
        "Title not applied correctly"
    )

    plt.close(fig)  # Close the figure after test
