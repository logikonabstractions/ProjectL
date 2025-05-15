import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')  # or 'Agg', 'Qt5Agg'


def plot_image(array, title=""):
    """ matplotlib to represent each card"""

    plt.imshow(array, cmap='winter')
    plt.title(title)
    plt.grid(False)  # Set to True if you want to see the grid lines
    plt.show()