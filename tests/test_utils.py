import pytest
from datetime import datetime, timedelta
from dynairxvis.utils import _plot_now_line
import matplotlib.pyplot as plt

CATEGORIES = ['N1', 'N2', 'N3']
VALUES = [10, 15, 35]


def test_plot_now_line_with_valid_ax():
    fig, ax = plt.subplots()
    _plot_now_line(ax)
    assert len(ax.lines) == 1
    assert ax.lines[0].get_color() == 'red'
    assert ax.lines[0].get_linestyle() == '--'
    assert ax.lines[0].get_linewidth() == 1


def test_plot_now_line_with_max_date():
    fig, ax = plt.subplots()
    max_date = datetime.now() + timedelta(days=180)
    _plot_now_line(ax, max_date=max_date)
    assert len(ax.lines) == 1
    assert ax.lines[0].get_color() == 'red'
    assert ax.lines[0].get_linestyle() == '--'
    assert ax.lines[0].get_linewidth() == 1


def test_plot_now_line_with_invalid_ax():
    with pytest.raises(TypeError):
        _plot_now_line(None)


def test_plot_now_line_with_invalid_max_date():
    fig, ax = plt.subplots()
    with pytest.raises(TypeError):
        _plot_now_line(ax, max_date="invalid_date")


def test_plot_now_line_with_label():
    fig, ax = plt.subplots()
    _plot_now_line(ax, label='Test Label')
    assert len(ax.texts) == 1
    assert ax.texts[0].get_text() == 'Test Label'
    assert ax.texts[0].get_color() == 'red'
