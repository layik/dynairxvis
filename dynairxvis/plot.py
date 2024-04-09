import os
import matplotlib.pyplot as plt
from .radar import radar


# =============================================================================
# Internal
# =============================================================================
def _draw_fig(filename=None, overwrite=False, **kwargs):
    """
    Internal function, which is called to draw a plot to the screen or
    save it in a file.

    Parameters
    ----------
    filename : str, optional
        The filename for the figure. If None, the figure is displayed
        on the screen.
    overwrite : bool, optional
        If False, does not overwrite the file if it exists. If True,
        overwrites the file.
    **kwargs : dict
        Keyword arguments for fig.savefig().

    Returns
    -------
    None.
    """
    if filename is not None:
        if overwrite or not os.path.isfile(filename):
            fig = plt.gcf()
            fig.savefig(filename, **kwargs)
        else:
            print('** WARNING **: Figure not saved because a file with the' +
                  'supplied name already exists.')
            print(filename)
    else:
        plt.show()


def plot(plot_name, categories, values, filename=None, overwrite=False,
         **kwargs):
    """
    High-level plotting function that decides which plotting function to call
    based on plot_name. Currently supports a 'radar' plot.

    Parameters
    ----------
    plot_name : str
        The name of the plot type to generate. Supported: 'radar'.
    categories : list
        The categories to be used in the plot.
    values : list
        The values associated with each category.
    filename : str, optional
        The filename for saving the plot. If None, the plot is shown on screen.
    overwrite : bool, optional
        If False, does not overwrite the file if it exists. If True,
        overwrites the file.
    **kwargs : dict
        Additional keyword arguments passed to the plot's savefig method.

    Returns
    -------
    None.
    """
    # Switch based on plot_name
    if plot_name == 'radar':
        radar(categories, values)
    else:
        print('**WARNING: ** no plot_name provided')

    # Show the plot or save it to a file
    _draw_fig(filename=filename, overwrite=overwrite, **kwargs)
