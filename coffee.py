# -*- coding: utf-8 -*-
"""
.. module:: coffee
   :synopsis: Describes a model that approximates a cup of coffee's rate of cooling as a function of time.

.. moduleauthor:: Huginn
"""

#~ Modules
from coffee_plot import coffee_plot as cplot
from viz.display.plot import plot
from copy import copy
import  os, sys, atexit, \
        matplotlib.pyplot as plt, \
        numpy as np
#/~ Modules

#~ Setup
# Make sure the working directory is set to this script's location.
os.chdir(os.path.dirname(sys.argv[0]))
# Make sure any open plots are closed when this script ends.
atexit.register(lambda destruct: plt.close(), None)
#/~ Setup

#~ Functions
def model(t0=0, tf=30, dt=.1, T0=90, Tf=70, Tp=75, Te=-5, experiments=8):
    """ Models the rate of cooling of coffee over time.

        :param t0: The inital time of Temperature measurement.
        :param tf: The maximum amount of time allotted for cooling.
        :param dt: The time differential.
        :param T0: The initial temperature of the object.
        :param Tf: The temperature equilibrium.
        :param Tp: The preferred temperature of the object.
        :param Te: The immediate change in temperature upon experiment.
        :param experiments: The number of intervals to conduct an experiment; add cream.
    """
    # Get 'indices' for cream experiments. Biased towards earlier time-points.
    tm = (tf-t0) / 4.
    offset = tm / experiments
    indices = np.arange(t0+offset, tm+offset, offset)
    indices = [indices[i] for i in range(experiments)]
    indices = reversed(indices)

    # Initialize dictionaries with time steps.
    times = {}
    times['black'] = np.arange(t0,tf,dt)
    times['cream'] = times['black'][[int(i*(1/dt)) for i in indices]]

    return cool(times, t0, dt, T0, Tf, Tp, Te)

def cool(times, t0, dt, T0, Tf, Tp, Te):
    """  Calculates a set of Temperature values given some initial conditions and calculated constants.

        :param times: A dictionary of time measurements. ('black':interval, 'cream':samples of 'black')
        :param t0: The inital time of Temperature measurement.
        :param dt: The time differential.
        :param T0: The initial temperature of the object.
        :param Tf: The temperature equilibrium.
        :param Tp: The preferred temperature of the object.
        :param Te: The immediate change in temperature upon experiment.
    """
    # Defines a lambda function that calculates each new temperature.
    _cool = lambda current,final,constant,delta: (current - constant*(current - final)*delta)

    # Retrieve the 'sample data' and calculated thermal constants.
    data_times, (data_Temps_b, data_Temps_c), constants = sample_data()

    # Define 'super' lists to store the results of multiple experiments.
    super_times, super_Temps = [list(data_times), list(data_times)], [list(data_Temps_b), list(data_Temps_c)]
    # Define 'sub' lists to store the result of an experiment.
    sub_times, sub_Temps = [t0], [T0]
    
    just_right = False   # Not too hot; maybe a little cold.
    for tb in times['black']:   # For every time allotted for coffee cooling...
        # The current Temperature.
        Tc = sub_Temps[-1]
        # The cooling constant of black coffee.
        cb = constants['black'] 
        # The next Temperature according to the difference equation.
        Tn = _cool(Tc, Tf, cb, dt)

        # Log and save the the time/Temp when the coffee is "just right".
        if not just_right and Tp != None and (Tn+Te) <= Tp:
            just_right = True

            print "\n~ Add Cream ~"
            print "Preferred Temperature = "+str(Tp)+"°C"
            print "Current Temperature = "+str(Tn)+"°C"
            print "Current Time = " + str(tb) +" minutes\n"

            times['cream'] = np.concatenate(([tb], times['cream']))

        sub_times.append(tb)
        sub_Temps.append(Tn)

    super_times.append(sub_times)
    super_Temps.append(sub_Temps)

    for tc in times['cream']:   # For every chosen time to add cream to the coffee...
        # Find the index of 'tc' in times['black']. 
        index = int(np.where(times['black'] == tc)[0])

        # List of times starting from 'index'.         |    # Insert a duplicate time.
        sub_times = copy(super_times[2][index:]);      sub_times[1:1] = [sub_times[0]]
        # List of Temps starting from 'index'.         |    # Insert a duplicate Temp and add cream to T_i=1.
        sub_Temps = copy(super_Temps[2][index:]);      sub_Temps[1:1] = [sub_Temps[0]+Te]

        for i in range(2,len(sub_times)):   # Calculate the Temps of the creamed coffee...
            # The current Temperature.
            Tc = sub_Temps[i-1]
            # The cooling constant of cooled coffee.
            cc = constants['cream']
            # The next Temperature according to the difference euqation.
            Tn = _cool(Tc, Tf, cc, dt)

            sub_Temps[i] = Tn

        super_times.append(sub_times)
        super_Temps.append(sub_Temps)

    return super_times, super_Temps, constants

def sample_data(data=None):
    """ Calculates thermal constants from a dataset.
        
        :param data: The dataset used to derive cooling constants. If 'None' use default 'data'.
    """

    if data == None:    # Use default 'data' if none is provided by user.
        data = np.array([[  0. ,  82.3,  68.8], [  2. ,  78.5,  64.8],
                         [  4. ,  74.3,  62.1], [  6. ,  70.7,  59.9],
                         [  8. ,  67.6,  57.7], [ 10. ,  65. ,  55.9],
                         [ 12. ,  62.5,  53.9], [ 14. ,  60.1,  52.3],
                         [ 16. ,  58.1,  50.8], [ 18. ,  56.1,  49.5],
                         [ 20. ,  54.3,  48.1], [ 22. ,  52.8,  46.8],
                         [ 24. ,  51.2,  45.9], [ 26. ,  49.9,  44.8],
                         [ 28. ,  48.6,  43.7], [ 30. ,  47.2,  42.6],
                         [ 32. ,  46.1,  41.7], [ 34. ,  45. ,  40.8],
                         [ 36. ,  43.9,  39.9], [ 38. ,  43. ,  39.3],
                         [ 40. ,  41.9,  38.6], [ 42. ,  41. ,  37.7],
                         [ 44. ,  40.1,  37. ], [ 46. ,  39.5,  36.4]])

    times = data[:,0]
    Temps_black = data[:,1]
    Temps_cream = data[:,2]

    # The cooling constants of 'black' and 'cream' coffee.
    cb = 0.
    cc = 0.
    for i in range(len(times)-1): # Iterate through every sample vector in the dataset.
        # Calculate delta time. (In case non-uniform)
        dt = times[i+1] - times[i]

        # Calculate thermal constants at each moment, for both cases.
        cb -= (Temps_black[i+1] - Temps_black[i]) / ((Temps_black[i] - 20)*dt)
        cc -= (Temps_cream[i+1] - Temps_cream[i]) / ((Temps_cream[i] - 20)*dt)

    # Average the cooling constants.
    cb /= (len(times)-1); print "Black Coffee (c):\t" + str(cb)
    cc /= (len(times)-1); print "Cream Coffee (c):\t" + str(cc)

    return times, (Temps_black, Temps_cream), {'black': cb, 'cream': cc}

#~ Entry point of the script.
if __name__ == "__main__":
    t0 = 0          # Begin modeling the Temperature at t=0 minutes.
    tf = 40         # Stop modeling the Temperature at tf=40 minutes.
    dt = .001       # Between t0 and tf, conduct a calculation for every dt.
    T0 = 90         # Assume the coffee is initially 90 °C.
    Tf = 20         # Assume the coffee's final temperature will be room temperature (20 °C).
    Tp = 75         # We want to drink the coffee when it is 75 °C.

    times, Temps, constants = model(t0, tf, dt, T0, Tf, Tp)
    
    dec = lambda x: len(str(x/10.).split('.')[0])

    t_min = times[0][0]
    t_max = round(times[0][-1], -dec(times[0][-1]))
    T_min = min(Temps[0][-1], Temps[1][-1])
    T_min = round(T_min, -dec(T_min)) - 10.*dec(T_min)
    T_max = max(Temps[0][0], Temps[1][0])
    T_max = round(T_max, -dec(T_max)) + 10.*dec(T_max)

    # Calculate the number of seconds from the decimal minutes.
    best_time = times[3][0]
    best_seconds = (best_time - float(str(best_time).split('.')[0]))*60.
    best_seconds = str(int(best_seconds))

    titles = [r"Discrete Time Model: $\Delta t="+str(dt)+"$ minutes; $\epsilon\propto\Delta t$",
              r"Sample Data: $\Delta t=2$ minutes; $\epsilon\propto\Delta t$"]

    plot(times, Temps,
        suptitle="Coffee Cooling",
        titles=titles,
        xlabels=["Time (minutes)"],
        ylabels=["Temperature ("+u'\N{DEGREE SIGN}'+"C)"],
        xbounds=[(t0,20), (t_min,t_max)],
        ybounds=[(70,T0), (T_min,T_max)],
        legends=[["Black Coffee", "Cream Coffee", "Cream Added",
                  r"$t^*\approx "+str(best_time)[:dec(best_time)]+"$ minutes and $"+best_seconds+"$ seconds"
                 ],
                 [r"Black Coffee: $\bar{c_{\mathbb{B}}}\approx"+str(constants['black'])[:6]+"$", # What are the units of 'c_B'?
                  r"Cream Coffee: $\bar{c_{\mathbb{C}}}\approx"+str(constants['cream'])[:6]+"$"
                 ]],
        custom=cplot)