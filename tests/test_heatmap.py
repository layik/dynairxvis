import numpy as np
from dynairxvis.plot import heatmap
import matplotlib.pyplot as plt
from unittest.mock import patch


@patch('matplotlib.pyplot.show')
def test_heatmap_creates_correct_matrix(mock_show):
    # Improved flattening function that checks type of each item
    def flatten(values):
        flattened_values = []
        for item in values:
            if isinstance(item, list):
                flattened_values.extend(item)
            else:
                flattened_values.append(item)
        return flattened_values
    # Define the categories and values to test
    categories = ['Cat A', 'Cat B', 'Cat C']
    values = [10, [15, 20], 35]

    # Expected matrix size
    expected_matrix_size = (len(categories), len(set(flatten(values))))

    # Call the heatmap function to simulate the heatmap creation
    # Since heatmap does not return a value, we'll need to capture
    # the matrix from the plotting context
    heatmap(categories, values, colorbar=False)
    # Access the current figure and its axes to get the matrix data
    fig = plt.gcf()
    ax = plt.gca()
    cax = ax.get_children()[0]  # Get the AxesImage object, the heatmap
    heatmap_matrix = cax.get_array().data  # Extract the data of the heatmap

    # Check if the created heatmap matrix has the correct size
    assert heatmap_matrix.shape == expected_matrix_size, (
        f"Expected matrix size {expected_matrix_size}, got {heatmap_matrix.shape}")

    # Cleanup after test
    plt.close(fig)
