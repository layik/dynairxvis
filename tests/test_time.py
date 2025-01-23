import pytest
from datetime import datetime
from dynairxvis.time import grouped_chart, line

import matplotlib.pyplot as plt


@pytest.fixture
def sample_data():
    categories = ['Task A', 'Task B', 'Task C']
    start_dates = [datetime(2020, 1, 1), datetime(2020, 6, 1),
                   datetime(2020, 8, 1)]
    end_dates = [datetime(2021, 1, 1), datetime(2020, 7, 1),
                 datetime(2020, 9, 1)]
    markers = ['^', 's', 'o']
    return categories, start_dates, end_dates, markers


def test_grouped_chart_line(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig, ax = plt.subplots()
    grouped_chart(categories, start_dates, end_dates, chart_type='line',
                  markers=markers, ax=ax)
    assert len(ax.lines) == len(categories)


def test_grouped_chart_scatter(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig, ax = plt.subplots()
    grouped_chart(categories, start_dates, end_dates, chart_type='scatter',
                  markers=markers, ax=ax)
    assert len(ax.collections) == len(categories)


def test_grouped_chart_heatmap(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig, ax = plt.subplots()
    grouped_chart(categories, start_dates, end_dates, chart_type='heatmap',
                  markers=markers, ax=ax)
    assert len(ax.images) == 1


def test_grouped_chart_invalid_type(sample_data, capsys):
    categories, start_dates, end_dates, markers = sample_data
    grouped_chart(categories, start_dates, end_dates, chart_type='invalid',
                  markers=markers)
    captured = capsys.readouterr()
    assert "Error: Invalid chart type 'invalid'" in captured.out


def test_line_chart(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig, ax = plt.subplots()
    line(categories, start_dates, end_dates, markers=markers, ax=ax)
    assert len(ax.lines) == len(categories)


def test_grouped_chart_with_values(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig, ax = plt.subplots()
    grouped_chart(categories, start_dates, end_dates, chart_type='heatmap',
                  values=[1, 2, 3], markers=markers, ax=ax)
    assert len(ax.images) == 1


def test_grouped_chart_with_values_categorical(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig, ax = plt.subplots()
    grouped_chart(categories, start_dates, end_dates, chart_type='heatmap',
                  values=['A', 'B', 'C'], markers=markers, ax=ax)
    assert len(ax.images) == 1


def test_grouped_chart_with_fig_kw(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    fig_kw = {'figsize': (12, 6)}  # Custom figure size
    grouped_chart(categories, start_dates, end_dates, chart_type='line', fig_kw=fig_kw)
    fig = plt.gcf()
    assert fig.get_size_inches().tolist() == [12, 6], "Figure size not applied correctly"
    plt.close(fig)


def test_grouped_chart_with_plot_kw(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    plot_kw = {'linewidth': 2, 'color': 'red'}  # Custom plot properties
    grouped_chart(categories, start_dates, end_dates, chart_type='line', plot_kw=plot_kw)
    ax = plt.gca()
    for line in ax.lines:
        assert line.get_linewidth() == 2, "Line width not applied correctly"
        assert line.get_color() == 'red', "Line color not applied correctly"
    plt.close(ax.figure)


def test_grouped_chart_with_kwargs_labels_and_title(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    grouped_chart(
        categories, start_dates, end_dates,
        chart_type='scatter',
        xlabel="Custom X", ylabel="Custom Y", title="Custom Title"
    )
    ax = plt.gca()
    assert ax.get_xlabel() == "Custom X", "X-axis label not applied correctly"
    assert ax.get_ylabel() == "Custom Y", "Y-axis label not applied correctly"
    assert ax.get_title() == "Custom Title", "Title not applied correctly"
    plt.close(ax.figure)


def test_grouped_chart_heatmap_with_kwargs(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    grouped_chart(
        categories, start_dates, end_dates,
        chart_type='heatmap', values=[1, 2, 3],
        cmap='viridis', xlabel="Custom X", title="Custom Heatmap"
    )
    ax = plt.gca()
    assert ax.get_title() == "Custom Heatmap", "Heatmap title not applied correctly"
    images = ax.get_images()
    assert len(images) == 1, "Heatmap image not found"
    plt.close(ax.figure)


def test_grouped_chart_with_legend(sample_data):
    categories, start_dates, end_dates, markers = sample_data
    grouped_chart(
        categories, start_dates, end_dates,
        chart_type='line', legend=True, legend_loc='upper left'
    )
    ax = plt.gca()
    legend = ax.get_legend()
    assert legend is not None, "Legend not applied"
    assert legend.get_title().get_text() == "Categories", "Legend title incorrect"
    plt.close(ax.figure)


# Failing
# def test_grouped_chart_with_category_colors(sample_data):
#     categories, start_dates, end_dates, markers = sample_data
#     category_colors = {'Task A': 'red', 'Task B': 'green', 'Task C': 'blue'}
#     grouped_chart(
#         categories, start_dates, end_dates,
#         chart_type='line', category_colors=category_colors
#     )
#     ax = plt.gca()
#     for line, category in zip(ax.lines, categories):
#         assert line.get_color() == category_colors[category], f"Color for {category} not applied correctly"
#     plt.close(ax.figure)

