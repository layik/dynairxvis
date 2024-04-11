import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from unittest.mock import patch
from datetime import datetime
from dynairxvis.plot import gantt


@patch('matplotlib.pyplot.show')
def test_gantt_chart(mock_show):
    categories = ['Task A', 'Task B', 'Task C']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1), datetime(2020, 8, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1), datetime(2020, 9, 1)]

    # Call the gantt function
    gantt(categories, start_dates, end_dates)

    # Obtain the current figure and axes
    fig = plt.gcf()
    ax = plt.gca()

    # Assertions
    # Check if a figure and axes are created
    assert fig is not None, "No figure was created"
    assert ax is not None, "No axes were created"

    # Check if the correct number of bars (tasks) are created
    assert len(ax.patches) == len(categories), "Incorrect number of tasks (bars) created"

    # Verify that the date formatter is set correctly
    assert isinstance(ax.xaxis.get_major_formatter(), mdates.DateFormatter), "X-axis is not using a DateFormatter"

    # Verify labels and titles
    assert ax.get_xlabel() == 'Time', "X-axis label is not set correctly"
    assert ax.get_title() == 'Gantt Chart', "Chart title is not set correctly"

    # Optionally, check that each task's bar starts at the correct position
    for patch, start_date in zip(ax.patches, start_dates):
        bar_start = mdates.num2date(patch.get_x()).replace(tzinfo=None)
        assert bar_start == start_date, f"Bar does not start at the correct date: expected {start_date}, got {bar_start}"

    plt.close(fig)  # Clean up by closing the figure
