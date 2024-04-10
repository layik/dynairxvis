import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import dot
from .test_utils import VALUES


@patch('matplotlib.pyplot.show')
def test_dot_creates_correct_number_of_dots(mock_show):
    # or use VALUES = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    dot(VALUES)

    fig = plt.gcf()
    assert len(fig.axes) > 0, "No axes found in the plot"
    ax = fig.axes[0]  # Get the first (and in this case, only) axes object

    # Get unique values and their counts in VALUES
    unique_values, counts = np.unique(VALUES, return_counts=True)

    # For each unique value, check if the correct number of dots is plotted
    for value, count in zip(unique_values, counts):
        # Extract the y-data for all dots plotted at the x-position
        # corresponding to 'value'
        # Extract the y-data for all dots plotted at the x-position
        plotted_dots_y = [
            line.get_ydata() for line in ax.get_lines()
            if line.get_xdata()[0] == value
        ]

    # Flatten the list of y-data arrays and count the number of dots
    num_plotted_dots = sum(len(y) for y in plotted_dots_y)
    error_msg = (
        f"Incorrect number of dots plotted for value {value}: "
        f"expected {count}, got {num_plotted_dots}"
    )
    assert num_plotted_dots == count, error_msg
