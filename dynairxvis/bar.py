from .scatter import scatter


def bar(categories, values, horizontal=False, markers=None,
        fig_kw={}, plot_kw={}, **kwargs):
    """
    Creates and displays a bar chart with quantities on the y-axis and
    nominal categories on the x-axis. Supports both vertical and horizontal
    orientations.

    Parameters
    ----------
    categories : list of str
        The nominal categories on the x-axis for vertical bars or
        y-axis for horizontal bars.
    values : list of int or float
        The quantitative values for each category.
    horizontal : bool, optional
        Determines the orientation of the bars. True for horizontal bars,
        False (default) for vertical bars.
    markers : dict, optional
        A dictionary mapping categories to custom marker styles, which will
        affect the appearance of the bar tops if displayed.
    fig_kw : dict
        Keyword arguments for plt.subplots() to customize the figure.
    plot_kw : dict
        Keyword arguments for ax.bar() to further customize the bar chart.
    **kwargs : dict
        Additional keyword arguments for customization not related to ax.bar().

    Example
    -------
    categories = ['Category A', 'Category B', 'Category C']
    values = [10, 20, 30]

    bar(categories, values, horizontal=True)
    """

    # Call the scatter function with mode set to 'bar'
    orientation = 'horizontal' if horizontal else 'vertical'

    scatter(categories, values=values, mode='bar', markers=markers,
            fig_kw=fig_kw, plot_kw=plot_kw, orientation=orientation, **kwargs)
