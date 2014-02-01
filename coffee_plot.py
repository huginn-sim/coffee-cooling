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

def coffee_plot(fig, axes, times, Temps, legends):
    if legends != None:
        legend = legends[0]
        black, cream, added = "Black Coffee", "Cream Coffee", "Cream Added"
        best = max(legend.keys(), key=len)
        legendary = True

    analysis_ax, data_ax = axes[0], axes[1]
    #~ Cream Coffee (at various times)
    for i,(time,Temp) in enumerate(zip(times,Temps)[4:-1]):
        cream_mark0, = analysis_ax.plot(time, Temp, c='w', ls='-', lw=2.5)
        cream_mark1, = analysis_ax.plot(time, Temp, c='#C48B52', ls='-', lw=2, alpha=.5)

        if legendary and i == 0:
            legend[cream] = (cream_mark0,cream_mark1)#,cream_mark2,cream_mark3)

    #best_mark0, = analysis_ax.plot(times[3], Temps[3], c='b', ls='-', lw=2)#, alpha=.5)
    best_mark1, = analysis_ax.plot(times[3], Temps[3], 'w-', lw=6)
    #best_mark2, = analysis_ax.plot(times[3], Temps[3], 'b-', lw=3)
    best_mark2, = analysis_ax.plot(times[3], Temps[3], c='#C48B52', ls='-', lw=3)

    #~ Black Coffee (no cream)
    black_mark0, = analysis_ax.plot(times[2], Temps[2], 'k-', lw=6)
    black_mark1, = analysis_ax.plot(times[2], Temps[2], c='#5A352D', ls='-', lw=5)
    
    if legendary:
        legend[black] = (black_mark0,black_mark1)

    #~ Cream Coffee (points of cream addition)
    for i,(time,Temp) in enumerate(zip(times,Temps)[4:-1]):
        cream_point_mark0, = analysis_ax.plot(time[0], Temp[0], 'ko', ms=10)
        cream_point_mark1, = analysis_ax.plot(time[0], Temp[0], c='#C48B52', marker='o', ms=8)
        
        if legendary and i == 0:
            legend[added] = (cream_point_mark0,cream_point_mark1)

    #~ Best Mark (Contd.)
    best_mark4, = analysis_ax.plot(times[3][0], Temps[3][0], 'w*', ms=30)
    best_mark5, = analysis_ax.plot(times[3][0], Temps[3][0], c='#C48B52', marker='*', ms=16)
    
    if legendary:
        legend[best] = (best_mark1,best_mark2,best_mark4,best_mark5)
    
    analysis_ax.set_axisbelow(True)
    # configure_plot(ax=analysis_ax,
    #                title=titles[0],
    #                xlabel=xlabels[0],
    #                ylabel=ylabels[0],
    #                xbounds=(0, 20),#xbounds[0]
    #                ybounds=(70, 90))#ybounds[0])

    analysis_ax.legend([legend[black], legend[cream], legend[added], legend[best]],
               [black, cream, added, best],
               numpoints=1)

    if data_ax != None:
        plt.sca(data_ax)
        
        legendary = False
        if legends != None and legends[1] != None:
            legend = legends[1]
            legendary = True
        
        #~ Black Coffee (no cream)
        black_mark0, = data_ax.plot(times[0], Temps[0], 'k', lw=6)
        black_mark1, = data_ax.plot(times[0], Temps[0], c='#5A352D', marker='o', ms=10, ls='-', lw=5)
        cream_mark0, = data_ax.plot(times[1], Temps[1], 'k', lw=6)
        cream_mark1, = data_ax.plot(times[1], Temps[1], c='#C48B52', marker='o', ms=10, ls='-', lw=5)

        data_ax.set_axisbelow(True)
        
        #data_ax.set_yscale("log")
        
        if legendary:
            data_ax.legend([(black_mark0, black_mark1), (cream_mark0, cream_mark1)], sorted(legend.keys()), numpoints=1)