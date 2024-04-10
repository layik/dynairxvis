import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from unittest.mock import patch
from datetime import datetime
from dynairxvis.plot import gantt

# You might need to adjust the import path based on your package structure


@patch('matplotlib.pyplot.show')
def test_gantt_chart(mock_show):
    categories = ['Task A', 'Task B', 'Task C']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
                   datetime(2020, 8, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
                 datetime(2020, 9, 1)]

    fig, ax = gantt(categories, start_dates, end_dates)

    # Check if a figure is created
    assert fig is not None, "No figure was created"

    # Check if bar collections are created (1 for each task)
    assert len(ax.containers) == len(categories), (
        "Not all tasks have a bar created")

    # Check dates on x-axis are formatted correctly
    xaxis_format = ax.xaxis.get_major_formatter()
    assert isinstance(xaxis_format, mdates.DateFormatter), (
        "X-axis is not using a DateFormatter")

    # Check the xlim is correctly set to include all tasks with some padding
    xlim = ax.get_xlim()
    expected_xlim = (
        mdates.date2num(min(start_dates)) - (
            mdates.date2num(max(end_dates)) - mdates.date2num(
                min(start_dates))) / 10,
        mdates.date2num(max(end_dates)) + (mdates.date2num(
            max(end_dates)) - mdates.date2num(min(start_dates))) / 10)
    assert xlim[0] <= expected_xlim[0] and xlim[1] >= expected_xlim[1], (
        "X-axis limits are not correctly set")

    # Check for correct labels and title
    assert ax.get_xlabel() == 'Time', "X-axis label is incorrect"
    assert ax.get_title() == 'Gantt Chart', "Chart title is incorrect"

    plt.close(fig)  # Close the figure after the test to clean up
