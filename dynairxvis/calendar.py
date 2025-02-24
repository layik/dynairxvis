import matplotlib.pyplot as plt
import numpy as np
from .time import grouped_chart
from .utils import FIG_SIZE, _resolve_orientation


def calendar(df=None, y_column=None, x_column=None, dot_size=0.2,
             ax=None, fig_kw={}, plot_kw={}, **kwargs):
    assert (df is not None), "Dataframe must be provided."
    assert (y_column is not None), "Y column must be provided."
    assert (x_column is not None), "X column must be provided."

    # Set up default figure settings
    default_fig_kw = FIG_SIZE
    default_fig_kw.update(fig_kw)
    chart_height = default_fig_kw['figsize'][1]
    chart_width = default_fig_kw['figsize'][0]

    # Use existing ax or create new figure and axis
    if ax is None:
        fig, ax = plt.subplots(**default_fig_kw)

    # TODO: enforce x column to be date
    df['year'] = df[x_column].dt.year
    g = df.groupby([y_column, 'year'], sort=False).size().unstack(fill_value=0)

    # Get list of diseases and years
    diseases = g.index.tolist()
    years = g.columns.tolist()

    # Ensure non-zero row heights and column widths
    min_row_height = 0.5
    min_col_width = 0.5

    row_height = max(chart_height / len(diseases), min_row_height)
    col_width = max(chart_width / len(years), min_col_width)

    # possible dot sizes
    te = len(df)
    possible_dot_size = np.sqrt((col_width * row_height) / te * 2)
    dot_size = min(dot_size, possible_dot_size)

    # Loop through diseases and years to draw cells and dots
    for i, disease in enumerate(diseases):
        for j, year in enumerate(years):
            count = g.at[disease, year]
            x_start = j * col_width
            y_start = i * row_height

            # Draw the background rectangle for the cell
            ax.add_patch(plt.Rectangle((x_start, y_start), col_width,
                                       row_height, color='white', ec='black'))

            # Calculate how many dots fit in this bin
            dots_per_row = max(int(col_width / dot_size), 1)
            dots_per_col = max(int(row_height / dot_size), 1)

            # Adjust dot size if necessary to ensure full space is used
            if dots_per_row * dots_per_col < count:
                dot_size = max(col_width / dots_per_row, 
                               row_height / dots_per_col)

            # Compute the final number of dots to be placed
            total_dots = min(count, dots_per_row * dots_per_col)

            for d in range(total_dots):
                x_offset = x_start + (d % dots_per_row) * dot_size + 0.1
                y_offset = y_start + (d // dots_per_row) * dot_size + 0.1
                if y_offset + dot_size < y_start + row_height and x_offset + dot_size < x_start + col_width:
                    ax.add_patch(plt.Rectangle((x_offset, y_offset), dot_size,
                                               dot_size, color='grey',
                                               ec='black'))

    # Set axis labels and limits
    ax.set_xlim(0, chart_width)
    ax.set_ylim(0, chart_height)
    ax.set_xticks([col_width * (j + 0.5) for j in range(len(years))])
    # TODO: give user choice to rotate labels
    ax.set_xticklabels(years, rotation=45)
    ax.set_yticks([row_height * (i + 0.5) for i in range(len(diseases))])
    ax.set_yticklabels(diseases)
    ax.set_xlabel(fig_kw.get('xlabel', 'Year'))
    ax.set_ylabel(fig_kw.get('ylabel', 'Disease'))
    ax.set_title(fig_kw.get('title', 'Calendar Heatmap'))

    # plt.rcParams.update({'font.size': 12})

    # If no ax provided, show the plot
    if ax is None:
        plt.tight_layout()
        plt.show()
