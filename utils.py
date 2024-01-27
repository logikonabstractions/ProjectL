import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')  # or 'Agg', 'Qt5Agg'


def plot_image(array, title=""):
    """ matplotlib to represent each card"""

    plt.imshow(array, cmap='winter')  # You can choose other colormaps like 'gray', 'plasma', etc.
    # plt.colorbar()  # Adds a color bar to indicate the values
    plt.title(title)
    plt.grid(False)  # Set to True if you want to see the grid lines
    plt.show()