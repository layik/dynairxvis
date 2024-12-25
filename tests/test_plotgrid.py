import matplotlib.pyplot as plt
from unittest.mock import patch
from datetime import datetime
from dynairxvis.plotgrid import plot_grid


@patch('matplotlib.pyplot.show')
def test_plot_grid_basic(mock_show):
    categories = ['Task A', 'Task B', 'Task C']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
                   datetime(2020, 8, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
                 datetime(2020, 9, 1)]

    plot_grid(
        categories_list=[categories],
        start_dates_list=[start_dates],
        end_dates_list=[end_dates],
        chart_types=['line']
    )

    fig = plt.gcf()
    ax = plt.gca()

    assert fig is not None, "No figure created for plot_grid"
    assert ax is not None, "No axes created for plot_grid"

    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_plot_grid_mismatch(mock_show):
    categories = ['Task A', 'Task B']
    start_dates = [datetime(2020, 1, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1)]

    plot_grid(
        categories_list=[categories],
        start_dates_list=[start_dates],
        end_dates_list=[end_dates],
        chart_types=['line', 'scatter']
    )

    fig = plt.gcf()
    assert fig is not None, "No figure created when lists mismatch"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_plot_grid_empty(mock_show):
    plot_grid(
        categories_list=[],
        start_dates_list=[],
        end_dates_list=[],
        chart_types=[]
    )
    mock_show.assert_not_called()


@patch('matplotlib.pyplot.show')
def test_plot_grid_partial(mock_show):
    categories = ['Task A', 'Task B']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1)]

    plot_grid(
        categories_list=[categories],
        start_dates_list=[start_dates],
        end_dates_list=[end_dates],
        chart_types=['line', 'scatter'],
        values_list=[[1, 2]]
    )

    fig = plt.gcf()
    assert fig is not None, "Figure should be created for partial lists"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_plot_grid_invalid_chart_type(mock_show):
    categories = ['Task A', 'Task B']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1)]

    plot_grid(
        categories_list=[categories],
        start_dates_list=[start_dates],
        end_dates_list=[end_dates],
        chart_types=['invalid']
    )

    mock_show.assert_not_called()


@patch('matplotlib.pyplot.show')
def test_plot_grid_with_titles(mock_show):
    categories = ['Task A', 'Task B']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1)]
    titles = ['Title 1', 'Title 2']

    plot_grid(
        categories_list=[categories, categories],
        start_dates_list=[start_dates, start_dates],
        end_dates_list=[end_dates, end_dates],
        chart_types=['line', 'scatter'],
        titles_list=titles
    )

    fig = plt.gcf()
    assert fig is not None, "Figure should be created with titles"
    plt.close(fig)


@patch('matplotlib.pyplot.show')
def test_plot_grid_with_fig_kw(mock_show):
    categories = ['Task A', 'Task B']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1)]
    fig_kw = {'figsize': (10, 5)}

    plot_grid(
        categories_list=[categories],
        start_dates_list=[start_dates],
        end_dates_list=[end_dates],
        chart_types=['line'],
        fig_kw=fig_kw
    )

    fig = plt.gcf()
    assert all(fig.get_size_inches() == (10, 5)), \
        "Figure size should be set by fig_kw"
    plt.close(fig)
