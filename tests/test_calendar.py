import pytest
import pandas as pd
import matplotlib.pyplot as plt
# Adjust the import to match your module's structure
from dynairxvis.plot import calendar


# Helper: create a sample DataFrame with datetime and categorical columns.
def create_sample_df():
    data = {
        'date': pd.to_datetime([
            '2021-01-01', '2021-01-01', '2021-06-01', '2022-01-01',
            '2022-02-15', '2021-12-31'
        ]),
        'disease': ['flu', 'flu', 'covid', 'covid', 'flu', 'covid']
    }
    return pd.DataFrame(data)


# Test 1: Verify that missing the dataframe raises an AssertionError.
def test_missing_dataframe():
    with pytest.raises(AssertionError, match="Dataframe must be provided."):
        calendar(df=None, y_column='disease', x_column='date')


# Test 2: Verify that missing the y_column raises an AssertionError.
def test_missing_y_column():
    df = create_sample_df()
    with pytest.raises(AssertionError, match="Y column must be provided."):
        calendar(df=df, y_column=None, x_column='date')


# Test 3: Verify that missing the x_column raises an AssertionError.
def test_missing_x_column():
    df = create_sample_df()
    with pytest.raises(AssertionError, match="X column must be provided."):
        calendar(df=df, y_column='disease', x_column=None)


# Test 4: Run calendar() with a provided Axes instance and check
# labels and patches.
def test_calendar_with_provided_ax():
    df = create_sample_df()
    fig, ax = plt.subplots(figsize=(8, 6))
    # Pass custom figure keywords to update labels and title.
    custom_fig_kw = {'xlabel': 'Year', 'ylabel': 'Disease',
                     'title': 'Test Heatmap'}
    calendar(df=df, y_column='disease', x_column='date', ax=ax,
             fig_kw=custom_fig_kw)

    # Check that axis labels and title are set as expected.
    assert ax.get_xlabel() == 'Year'
    assert ax.get_ylabel() == 'Disease'
    assert ax.get_title() == 'Test Heatmap'

    # Ensure that patches were added (background cells and dot patches).
    assert len(ax.patches) > 0, "Expected patches to be drawn on the Axes."


# Test 5: Run calendar() without providing an Axes
# instance (the function should create one).
def test_calendar_without_ax():
    df = create_sample_df()
    # Clear any existing figures.
    plt.close('all')

    # Call calendar without providing an Axes; it should create its own.
    calendar(df=df, y_column='disease', x_column='date')

    # Get the current Axes from matplotlib.
    current_ax = plt.gca()
    # Confirm that patches were added to the current Axes.
    assert len(current_ax.patches) > 0, "Expected patches in the current Axes \
        when no ax is provided."


# Optional Test 6: Check that the expected number of background
# rectangles is created.
def test_background_rectangles_count():
    df = create_sample_df()
    fig, ax = plt.subplots(figsize=(8, 6))
    calendar(df=df, y_column='disease', x_column='date', ax=ax)

    # The function groups by (disease, year).
    # For our sample, unique diseases and years are determined by the dates.
    # Calculate expected number of cells: (# of unique diseases)
    # x (# of unique years).
    df['year'] = df['date'].dt.year
    group = df.groupby(['disease', 'year']).size().unstack(fill_value=0)
    expected_cells = len(group.index) * len(group.columns)

    # In the code, one background rectangle (white with black edge)
    # is drawn per cell.
    # We extract background patches by filtering for color 'white'.
    bg_patches = [p for p in ax.patches if p.get_facecolor()[:3] == (
        1.0, 1.0, 1.0)]
    assert len(bg_patches) == expected_cells, f"Expected {expected_cells} \
        background cells but found {len(bg_patches)}."
