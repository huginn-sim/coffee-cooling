# -*- coding: utf-8 -*-
"""
.. module:: plot
   :synopsis: Provides a general interface for formatting plots of a multiple X,Y values.

.. moduleauthor:: Huginn
"""

#~ Modules
import  matplotlib.pyplot as plt, \
        numpy as np
#/~ Modules

#~ Functions
def configure(ax, title, xlabel, ylabel, xbounds, ybounds):
    """ Configures the plot with the specified parameters.

        :param ax: The current subplot to manipulate.
        :param title: The title of the current subplot.
        :param xlabel: The label of the x-axis.
        :param ylabel: The label of the y-axis.
        :param xbounds: The bounds of the x-axis.
        :param ybounds: The bounds of the y-axis.
    """
    if ax == None: return

    # Set title, gridlines, and labels.
    ax.set_title(title, size=20)
    ax.grid(True, "major", alpha=.6)
    ax.grid(True, "minor", alpha=.4)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Hide spines.
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set the limits of the x,y axes.
    if xbounds == None:
        xbounds = ax.get_xlim()
    if ybounds == None:
        ybounds = ax.get_ylim()

    x_offset = abs(xbounds[1] - xbounds[0])/50.
    y_offset = abs(ybounds[1] - ybounds[0])/50.
    ax.set_xlim((xbounds[0] - x_offset, xbounds[1] + x_offset))
    ax.set_ylim((ybounds[0] - y_offset, ybounds[1] + y_offset))

    # X - Position and set major/minor ticks.
    ax.xaxis.set_ticks_position('bottom')
    offset = ax.get_xticks()[1] - ax.get_xticks()[0]
    ax.set_xticks(np.arange(ax.get_xticks()[1]+offset/2., ax.get_xticks()[-2], offset), minor=True)
    ax.xaxis.set_tick_params(width=4, length=5, color='k')
    ax.xaxis.set_tick_params(which="minor", width=2, length=4, color='k')
    
    # Y - Position and set major/minor ticks.
    ax.yaxis.set_ticks_position('left')
    offset = ax.get_yticks()[1] - ax.get_yticks()[0]
    ax.set_yticks(np.arange(ax.get_yticks()[1] + offset/2., ax.get_yticks()[-2], offset), minor=True)
    ax.yaxis.set_tick_params(width=4, length=5, color='k')
    ax.yaxis.set_tick_params(which="minor", width=2, length=4, color='k')

    # Draw x,y axes.
    x_edge = (xbounds[1] - xbounds[0]) / ((xbounds[1] - xbounds[0]) + x_offset)
    y_edge = (ybounds[1] - ybounds[0]) / ((ybounds[1] - ybounds[0]) + y_offset)
    ax.axhline(ybounds[0] - y_offset, 1-x_edge, x_edge, lw=5, color="k", alpha=1.)
    ax.axvline(xbounds[0] - x_offset, 1-y_edge, y_edge, lw=4, color="k", alpha=1.)

def plot(X, Y, suptitle="", titles="", xlabels="", ylabels="", xbounds=None, ybounds=None, layout='tight', legends=None, custom=None):
    """ Plots the specified X,Y data and applies settings.
        If no 'custom' plotting function is defined, all (x,y) in zip(X,Y) are plotted on seperate subplots.

        :param X: A list of discrete experiments representing independent variables.
        :param Y: A list of discrete experiments representing dependent variables.
        :param suptitle: The main title of the figure.
        :param titles: The title(s) of the subplot(s).
        :param xlabels: The label(s) of the x-axis.
        :param ylabels: The label(s) of the y-axis.
        :param xbounds: One or two bounds of the x-axis.
        :param ybounds: One or two bounds of the y-axis.
        :param layout: An argument specifying figure margin presets.
        :param legends: Dictionaries specifying the labels of the plot 'legend'.
        :param custom: A user-defined function for plotting data and applying legends.
    """
    # Initially, assume that no legend will be generated.
    legendary = False
    if type(titles) == list and type(xlabels) == list and type(ylabels) == list and type(xbounds) == list and type(ybounds) == list:
        # Propogate plot-settings for every subplot, if necessary.
        if len(titles) == 1:
            titles = [titles[0], titles[0]]
        if len(xlabels) == 1:
            xlabels = [xlabels[0], xlabels[0]]
        if len(ylabels) == 1:
            ylabels = [ylabels[0], ylabels[0]]
        if len(xbounds) == 1:
            xbounds = [xbounds[0], xbounds[0]]
        if len(ybounds) == 1:
            ybounds = [ybounds[0], ybounds[0]]
        if type(legends) == list and len(legends) == 1:
            legends = [legends[0], legends[0]]

        fig, axes = plt.subplots(nrows=1, ncols=2, squeeze=True)
    elif type(titles) == str and type(xlabels) == str and type(ylabels) == str:
        # Default to single-value case if only one dataset is to be plotted.
        X = [X]; Y = [Y]
        titles = [titles]
        xlabels = [xlabels]; ylabels = [ylabels];
        xbounds = [xbounds]; ybounds = [ybounds];
        fig, ax = plt.subplots()
        axes = [ax]
    else:
        print "Invalid configuration. Read docstring for more information."
        return
    
    if custom != None:
        custom(X, Y, axes, legends)

    bundle = zip(axes,X,Y,titles,xlabels,ylabels,xbounds,ybounds)
    for ax,x,y,title,xlabel,ylabel,xbound,ybound in bundle:
        if ax != None and custom == None:
            ax.plot(x, y)
        configure( ax=ax,
                   title=title,
                   xlabel=xlabel,
                   ylabel=ylabel,
                   xbounds=xbound,
                   ybounds=ybound)

    if layout == 'tight':
        fig.suptitle(suptitle, size=30)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    else:
        fig.suptitle(suptitle)

    plt.show()

#/~ Functions.

#~ Entry point of the script.
if __name__ == "__main__":
    import math
    x = np.arange(0,math.pi*3,.001)
    y = np.cos(x)
    plot(X=x, Y=y,
         suptitle="Trig Plot", titles=r"$f\left( x\right)=cos\left( x\right)$",
         xlabels="x", ylabels=r"$f\left( x\right)$", layout=None)

    plot(x, y, layout=None)