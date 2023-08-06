# pragma: no cover
import tkinter as tk
import tkinter.ttk as ttk
import lazy_import

for module in [
    "mayavi",
    "pandas",
    "scipy.linalg",
    "scipy.ndimage",
    "scipy.optimize",
    "scipy.stats",
    "scipy.signal",
    "skimage.measure",
    "skimage.morphology",
    "scipy",
    "skimage",
    "vtk",
]:
    lazy_import.lazy_module(module)


import sys
from ctpros.graphics import GUI


def main(argv):
    gui = GUI(*argv)
    gui.mainloop()


if __name__ == "__main__":
    main(sys.argv[1:])
