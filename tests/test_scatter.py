import matplotlib.pyplot as plt
from unittest.mock import patch
from datetime import datetime
from dynairxvis.plot import scatter


@patch('matplotlib.pyplot.show')
def test_scatter(mock_show):
    categories = ['Task A', 'Task B', 'Task C']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
                   datetime(2020, 8, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
                 datetime(2020, 9, 1)]
    markers = {'Task A': '^', 'Task B': 's', 'Task C': 'o'}

    # Call the function without trying to unpack fig and ax
    scatter(categories, start_dates, end_dates, markers)

    # Obtain the current figure and axes
    fig = plt.gcf()
    ax = plt.gca()

    # Check if a figure and axis are created
    assert fig is not None, "No figure was created"
    assert ax is not None, "No axes were created"

    # Close the figure after the test
    plt.close(fig)
