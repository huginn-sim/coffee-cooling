# -*- coding: utf-8 -*-
"""
.. module:: coffee_plot
   :synopsis: TODO.

.. moduleauthor:: Huginn
"""

#~ Modules
import  matplotlib.pyplot as plt, \
        numpy as np
#/~ Modules

def coffee_plot(times, Temps, axes, legends=[None, None], split=2):
    plot_model(times[split:], Temps[split:], axes[0], legends[0])
    plot_samples(times[:split], Temps[:split], axes[1], legends[1])

def plot_model(times, Temps, ax=None, legend=None):
    if ax != None: plt.sca(ax)
    else: ax = plt.gca()

    # Initially, assume there is no legend.
    legendary = False
    if legend != None:
        _legend = dict.fromkeys(legend)
        black, cream, added, best = legend
        legendary = True
        
    #~ Cream Coffee (at various times)
    for i,(time,Temp) in enumerate(zip(times,Temps)[3:]):
        cream_mark0, = ax.plot(time, Temp, c='w', ls='-', lw=2.5)
        cream_mark1, = ax.plot(time, Temp, c='#C48B52', ls='-', lw=2, alpha=.5)

        if legendary and i == 0:   # Create a legend symbol for this line. 
            _legend[cream] = (cream_mark0,cream_mark1)

    #~ Best Time to Add Cream
    best_mark0, = ax.plot(times[1], Temps[1], 'w-', lw=6)
    best_mark1, = ax.plot(times[1], Temps[1], c='#C48B52', ls='-', lw=3)

    #~ Black Coffee (no cream)
    black_mark0, = ax.plot(times[0], Temps[0], 'k-', lw=6)
    black_mark1, = ax.plot(times[0], Temps[0], c='#5A352D', ls='-', lw=5)
    
    if legendary:   # Create a legend symbol for this line. 
        _legend[black] = (black_mark0,black_mark1)

    #~ Cream Coffee (points of cream addition)
    for i,(time,Temp) in enumerate(zip(times,Temps)[3:]):
        cream_point_mark0, = ax.plot(time[0], Temp[0], 'ko', ms=10)
        cream_point_mark1, = ax.plot(time[0], Temp[0], c='#C48B52', marker='o', ms=8)
        
        if legendary and i == 0:    # Create a legend symbol for this line.
            _legend[added] = (cream_point_mark0,cream_point_mark1)

    #~ Best Time (Contd.)
    best_mark2, = ax.plot(times[1][0], Temps[1][0], 'w*', ms=30)
    best_mark3, = ax.plot(times[1][0], Temps[1][0], c='#C48B52', marker='*', ms=16)
    
    if legendary:   # Create a legend symbol for the * symbol. 
        _legend[best] = (best_mark0,best_mark1,best_mark2,best_mark3)
    
    if legendary:   # Add the legends and labels to the plot.
        ax.legend([_legend[black], _legend[cream], _legend[added], _legend[best]],
                  [black, cream, added, best], numpoints=1)

def plot_samples(times, Temps, ax, legend=None):
    if ax != None: plt.sca(ax)
    else: ax = plt.gca()

    legendary = False
    if legend != None:
        _legend = dict.fromkeys(legend)
        legendary = True
    
    #~ Black Coffee (no cream)
    black_mark0, = ax.plot(times[0], Temps[0], 'k', lw=6)
    black_mark1, = ax.plot(times[0], Temps[0], c='#5A352D', marker='o', ms=10, ls='-', lw=5)
    cream_mark0, = ax.plot(times[1], Temps[1], 'k', lw=6)
    cream_mark1, = ax.plot(times[1], Temps[1], c='#C48B52', marker='o', ms=10, ls='-', lw=5)

    if legendary:   # Create a legend with the symbols and labels.
        ax.legend([(black_mark0, black_mark1), (cream_mark0, cream_mark1)],
                         sorted(_legend.keys()),
                         numpoints=1)