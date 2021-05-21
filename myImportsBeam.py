from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfile
from tkinter import *

import numpy as np
import pickle
import os

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
import matplotlib.animation as animation
from matplotlib import style
matplotlib.use("TkAgg")

# Styling for the plot
style.use("ggplot")
