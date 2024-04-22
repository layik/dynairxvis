import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import pie
from .test_utils import CATEGORIES, VALUES


@patch('matplotlib.pyplot.show')
def test_pie():
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
