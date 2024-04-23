# from unittest.mock import patch
# import os
# from dynairxvis.plot import plot
# from .test_utils import CATEGORIES, VALUES


# @patch('matplotlib.pyplot.show')
# def test_plot_saves_file(mock_show):
#     # When function calls plt.show(), it won't actually display the plot.
#     # Instead, plt.show() does nothing during this test,
#     # allowing the test to proceed without interruption.

#     # Test if the plot has been saved to a file
#     # This requires modifying the radar function to save the plot
#     filename = "test_plot.png"
#     plot('radar', CATEGORIES, VALUES, filename=filename)
#     assert os.path.isfile(filename), "Plot file was not created"
#     os.remove(filename)  # Clean up the file after test


# @patch("builtins.print")
# def test_invalid_plot_name(mock_print):
#     plot('foo', CATEGORIES, VALUES)
#     mock_print.assert_called_with("**WARNING: ** 'foo' is not" +
#                                   " a supported plot type.")
