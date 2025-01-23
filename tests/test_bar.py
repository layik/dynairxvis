import matplotlib.pyplot as plt
from unittest.mock import patch
from dynairxvis.plot import bar
from .test_utils import CATEGORIES, VALUES
import numpy as np


@patch('matplotlib.pyplot.show')
def test_bar(mock_show):
    # Test default (vertical orientation)
    bar(CATEGORIES, VALUES)
    fig = plt.gcf()
    ax = plt.gca()
    assert fig is not None, "No figure created with default parameters"
    assert ax is not None, "No axes created with default parameters"
    assert len(ax.containers) > 0, "No bars created with default parameters"
    plt.close(fig)

    # Test horizontal orientation
    bar(CATEGORIES, VALUES, horizontal=True)
    ax = plt.gca()
    assert len(ax.patches) > 0, "No horizontal bars created"
    plt.close(fig)

    # Test fig_kw
    bar(CATEGORIES, VALUES, fig_kw={"figsize": (10, 6)})
    fig = plt.gcf()
    assert np.allclose(fig.get_size_inches(), (10, 6)), (
        "fig_kw not applied correctly"
    )
    plt.close(fig)

    # Test plot_kw
    bar(CATEGORIES, VALUES, plot_kw={"color": "red", "alpha": 0.5})
    ax = plt.gca()
    for container in ax.containers:
        for bar_patch in container:
            assert bar_patch.get_facecolor() == (1.0, 0.0, 0.0, 0.5), (
                "plot_kw not applied correctly"
            )
    plt.close(fig)

    # Test additional kwargs
    bar(CATEGORIES, VALUES, title="Test Title", xlabel="Categories",
        ylabel="Values")
    ax = plt.gca()
    assert ax.get_title() == "Test Title", "Title not applied correctly"
    assert ax.get_xlabel() == "Categories", (
        "X-axis label not applied correctly"
    )
    assert ax.get_ylabel() == "Values", "Y-axis label not applied correctly"
    plt.close(fig)
