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


# def test_grouped_chart_with_values_categorical_bad(sample_data, capsys):
#     categories, start_dates, end_dates, markers = sample_data
#     fig, ax = plt.subplots()
#     grouped_chart(categories, start_dates, end_dates, chart_type='heatmap',
#                   values=['$C'], markers=markers, ax=ax)
#     captured = capsys.readouterr()
#     assert "Warning: 'values' must be numeric or ordered " \
#         "categorical to use for color scaling. Defaulting to grayscale." \
#         in captured.out


def test_grouped_chart_heatmap_with_category_colors(sample_data):
    categories, start_dates, end_dates, _ = sample_data
    fig, ax = plt.subplots()
    grouped_chart(categories, start_dates, end_dates, chart_type='heatmap',
                  ax=ax, values=[1, 2, 3],
                  category_colors=['red', 'green', 'blue'])
    assert len(ax.images) == 1
