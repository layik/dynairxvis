import unittest
from unittest.mock import patch
import pandas as pd
from dynairxvis.plot import plot_charts
import io
import sys

# Set the matplotlib backend to Agg
import matplotlib
matplotlib.use('Agg')


class TestPlotCharts(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Blood_Pressure': [120, 130, 125],
            'Condition': ['Diabetes', 'Hypertension', 'Asthma'],
            'Visit_Date': pd.to_datetime(
                ['2021-01-01', '2021-01-02', '2021-01-03']),
            'Pain_Scale': pd.Categorical(
                ['low', 'high', 'medium'], ordered=True)
        })

    @patch('matplotlib.pyplot.show')
    def test_plot_charts_histogram(self, mock_histogram):
        plot_charts(self.df, column_refs=['Blood_Pressure'])
        mock_histogram.assert_called()
        args, kwargs = mock_histogram.call_args
        print("Args:", args)
        print("Kwargs:", kwargs)

    @patch('matplotlib.pyplot.show')
    def test_plot_charts_bar(self, mock_bar):
        plot_charts(self.df, column_refs=['Condition', 'Blood_Pressure'])
        mock_bar.assert_called()
        args, kwargs = mock_bar.call_args
        print("Args:", args)
        print("Kwargs:", kwargs)

    def test_plot_charts_inappropriate_columns(self):
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        plot_charts(self.df, column_refs=['Visit_Date', 'Pain_Scale'])

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check the output
        output = captured_output.getvalue()
        self.assertIn(
            "No suitable plot type found for the columns or data types.",
            output)

    def tearDown(self):
        # Ensure stdout is restored if an error occurs during the test
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
