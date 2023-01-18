#!/usr/bin/env python
# coding: utf-8

# # Hamilton Holt
# This program generates a visualization of the Mandelbrot set, a mathematical set of complex numbers that exhibit complex behavior under certain operations. The code also includes a dropdown menu that allows the user to change the colormap of the plot, a slider widget that allows the user to adjust the maximum number of iterations used to calculate the Mandelbrot set, and buttons that allow the user to zoom in and out on the plot or reset the plot. The features are only interative if the code is ran in a separate Python environment. The plot is generated using the matplotlib library, and the dropdown menu and buttons are implemented using the ipywidgets and matplotlib.widgets libraries.

# In[26]:


import numpy as np
import matplotlib.pyplot as plt
# Create a complex grid of points
xmin, xmax, ymin, ymax = -2, 1, -1, 1
xx, yy = np.meshgrid(np.linspace(xmin, xmax, 1000), np.linspace(ymin, ymax, 1000))
z = xx + 1j * yy

# Initialize the Mandelbrot set to the grid of points
c = z

# Set the maximum number of iterations
max_iter = 50

# Initialize the escape value to be a large number
escape = 2**128

# Initialize an array to store the values of the Mandelbrot set
mandelbrot = np.full(z.shape, max_iter, dtype=int)

# Iterate over each point in the grid
for n in range(max_iter):
    # Check if the point has escaped
    mask = abs(z) > escape
    
    # If the point has escaped, set the value in the mandelbrot array to the number of iterations it took to escape
    mandelbrot[mask] = n
    
    # If the point has not escaped, update the value of z
    z[~mask] = z[~mask]**2 + c[~mask]

from ipywidgets import Dropdown
# Set up the dropdown menu callback function
def change_colormap(change):
    # Get the selected colormap
    colormap = change['new']
    
    # Set the colormap for the plot
    plt.cm.get_cmap(colormap)
    
    # Redraw the plot
    plt.draw()

# Add a dropdown menu to the plot
dropdown = Dropdown(options=["gray", "jet", "viridis", "magma"], value="gray", description="Colormap")
dropdown.observe(change_colormap, names='value')

# Display the dropdown menu
display(dropdown)

# Plot the Mandelbrot set using matplotlib
plt.imshow(mandelbrot.T, extent=(xmin, xmax, ymin, ymax))

# Add a colorbar to the plot
plt.colorbar()

# Add a title to the plot
plt.title("Mandelbrot Set")

# Set the x and y axis labels
plt.xlabel("Real")
plt.ylabel("Imaginary")

from matplotlib.widgets import Button
# Set up the zoom in button callback function
def zoom_in(event):
    # Get the current x and y limits of the plot
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()
    
    # Calculate the center of the plot
    xcen, ycen = (xlim[1] + xlim[0]) / 2, (ylim[1] + ylim[0]) / 2
    
    # Calculate the width and height of the plot
    width, height = xlim[1] - xlim[0], ylim[1] - ylim[0]
    
    # Calculate the zoom factor
    zoom_factor = 2
    
    # Update the x and y limits of the plot
    plt.gca().set_xlim(xcen - zoom_factor * width / 2, xcen + zoom_factor * width / 2)
    plt.gca().set_ylim(ycen - zoom_factor * height / 2, ycen + zoom_factor * height / 2)
    
    # Redraw the plot
    plt.draw()

# Set up the zoom out button callback function
def zoom_out(event):
    # Get the current x and y limits of the plot
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()
    
    # Calculate the center of the plot
    xcen, ycen = (xlim[1] + xlim[0]) / 2, (ylim[1] + ylim[0]) / 2
    
    # Calculate the width and height of the plot
    width, height = xlim[1] - xlim[0], ylim[1] - ylim[0]
    
    # Calculate the zoom factor
    zoom_factor = 2
    
    # Update the x and y limits of the plot
    plt.gca().set_xlim(xcen - zoom_factor * width / 2, xcen + zoom_factor * width / 2)
    plt.gca().set_ylim(ycen - zoom_factor * height / 2, ycen + zoom_factor * height / 2)
    
    # Redraw the plot
    plt.draw()

# Set up the reset button callback function
def reset(event):
    # Reset the x and y limits of the plot
    plt.gca().set_xlim(xmin, xmax)
    plt.gca().set_ylim(ymin, ymax)
    
    # Redraw the plot
    plt.draw()

# Add a zoom in button to the plot
axzoomin = plt.axes([0.7, 0.9, 0.1, 0.075])
bzoomin = Button(axzoomin, "Zoom In")
bzoomin.on_clicked(zoom_in)

# Add a zoom out button to the plot
axzoomout = plt.axes([0.8, 0.9, 0.1, 0.075])
bzoomout = Button(axzoomout, "Zoom Out")
bzoomout.on_clicked(zoom_out)

# Add a reset button to the plot
axreset = plt.axes([0.9, 0.9, 0.1, 0.075])
breset = Button(axreset, "Reset")
breset.on_clicked(reset)

from matplotlib.widgets import Slider
# Set up the slider callback function
def update(val):
    # Get the current value of the slider
    max_iter = int(val)
    
    # Recalculate the Mandelbrot set with the new value of max_iter
    z = xx + 1j * yy
    c = z
    mandelbrot = np.zeros(z.shape, dtype=int)
    for n in range(max_iter):
        mask = abs(z) > escape
        mandelbrot[mask] = n
        z[~mask] = z[~mask]**2 + c[~mask]
    
    # Update the plot with the new Mandelbrot set
    plt.imshow(mandelbrot.T, extent=(xmin, xmax, ymin, ymax))
    plt.draw()

# Add a slider widget to the plot
axiter = plt.axes([0.15, 0.01, 0.7, 0.03])
siters = Slider(axiter, 'Max Iterations', 1, 100, valinit=max_iter, valfmt='%d')
siters.on_changed(update)

# Show the plot
plt.show()

