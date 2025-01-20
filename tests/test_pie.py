import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import pie
from .test_utils import CATEGORIES, VALUES


@patch('matplotlib.pyplot.show')
def test_pie(mock_show):
    # Call the function without trying to unpack fig and ax
    pie(CATEGORIES, VALUES)

    # Obtain the current figure and axes
    fig = plt.gcf()
    axs = fig.axes

    # Check if a figure and axes are created
    assert fig is not None, "No figure was created"
    assert len(axs) == len(CATEGORIES), "Incorrect number of pie charts created"

    # Check for proper labels and values in the pies
    for ax, value in zip(axs, VALUES):
        wedges, texts = ax.patches, [text.get_text() for text in ax.texts]
        assert len(wedges) == 2, "Pie chart does not contain two segments"
        assert texts[0].startswith(str(value)), "Incorrect label on pie chart"

    # Close the figure after the test
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_pie_with_custom_fig_kw(mock_show):
    # Test custom figure size
    pie(CATEGORIES, VALUES, fig_kw={'figsize': (12, 6)})
    fig = plt.gcf()
    assert list(fig.get_size_inches()) == [12, 6], "Custom figure size not applied"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_pie_with_custom_colors_and_startangle(mock_show):
    # Test custom colors and start angle
    pie(CATEGORIES, VALUES, colors=['red', 'green'], startangle=180)
    fig = plt.gcf()
    ax = fig.axes[0]
    wedges = ax.patches
    assert len(wedges) == 2, "Pie chart does not have correct number of segments"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_pie_with_autopct(mock_show):
    # Test pie chart with percentages displayed
    pie(CATEGORIES, VALUES, autopct='%1.0f%%')
    fig = plt.gcf()
    ax = fig.axes[0]
    text_labels = [text.get_text() for text in ax.texts]
    assert any('%' in label for label in text_labels), "Percentage labels not applied"
    plt.close(fig)
