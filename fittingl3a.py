# -*- coding: utf-8 -*-
"""
This program imports data from the file specified by the string filename
The first line of the file is ignored (assuming it's the name of the variables)
After that the data file needs to be formatted: 
number space number space number space number newline
Do NOT put commas in your data file!!
The data file should be in the same directory as this python file
The data should be in the order:
x_data y_data x_uncertainty y_uncertainty
Then this program tries to fit a function to the data points
It plots the data as dots with errorbars and the best fit line
It then prints the best fit information
After that, it plots the "residuals": ydata - fittedfunction(xdata)
That is it subtracts your fitted ideal values from your actual data to see 
what is "left over" from the fit
Ideally your residuals graph should look like noise, otherwise there is more
information you could extract from your data (or you used the wrong fitting
function)
If you want to change the file name, that's the next line below this comment
"""

filename="LAB3/LAB3_Data.txt"
# change this if your filename is different


import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt
import math

def my_func(x, a, b, c):
    return a*(b+x)**c
# this is the function we want to fit. the first variable must be the
# x-data (length), the rest are the unknown constants we want to determine
def main():
    data=loadtxt(filename, usecols=(0,1,2,3), skiprows=1, unpack=True)
    # load file, take columns 0 & 1 & 2 & 3, skip 1 row, unpack=transpose x&y
    
    xdata=data[0]
    ydata=data[1]
    xerror=data[2]
    yerror=data[3]
    # finished importing data, naming it sensibly
               
    init_guess=(2.0, 0.00, 0.5)
    # your initial guess of (a, b, c)
    
    popt, pcov = optimize.curve_fit(my_func, xdata, ydata, p0=init_guess)
    # the best fit values are popt[], pcov[] tells us the uncertainties
    
    a=popt[0]
    b=popt[1]
    c=popt[2]
    # best fit values are named nicely
    u_a=pcov[0,0]**(0.5)
    u_b=pcov[1,1]**(0.5)
    u_c=pcov[2,2]**(0.5)    
    # uncertainties of fit are named nicely
        
    start=min(xdata)
    stop=max(xdata)    
    xs=np.arange(start,stop,(stop-start)/1000) # fit line has 1000 points
    curve=my_func(xs,a,b,c)
    # (x,y)=(xs,curve) is the line of best fit for the data in (xdata,ydata) 
    
    fig, (ax1,ax2) = plt.subplots(2, 1)
    # make 2 graphs above/below each other: ax1 is top, ax2 is bottom
    fig.subplots_adjust(hspace=0.6)
    # hspace is horizontal space between the graphs
    
    ax1.errorbar(xdata,ydata,yerr=yerror,xerr=xerror,fmt=".")
    # plot the data, fmt makes it data points not a line
    ax1.plot(xs,curve, label = "Power Law Function Fit")
    # plot the best fit curve on top of the data points as a line
    
    ax1.set_xlabel("String Length (m)")
    ax1.set_ylabel("Period (s)")
    ax1.set_title("Period vs. String Length from Pivot to Centre of Mass")
    ax1.legend()
    # HERE is where you change how your graph is labelled
    
    print("Results of fitting data to f(x)=a*(b+x)**c:")
    print("a:", a, "+/-", u_a, "theoretically 2")
    print("b:", b, "+/-", u_b, "theoretically 0")
    print("c:", c, "+/-", u_c, "theoretically 0.5")
    # prints the various values with uncertainties
    
    residual=ydata-my_func(xdata,a,b,c)
    # find the residuals
    zeroliney=[0,0]
    zerolinex=[start,stop]
    # create the line y=0
    
    correlation_matrix = np. corrcoef(xdata, ydata)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2.
    print(r_squared)

    ax2.errorbar(xdata,residual,yerr=yerror,xerr=xerror,fmt=".")
    # plot the residuals with error bars
    ax2.plot(zerolinex,zeroliney)
    # plot the y=0 line for context
    
    ax2.set_xlabel("xdata")
    ax2.set_ylabel("residuals of ydata")
    ax2.set_title("Residuals of the fit")
    # HERE is where you change how your graph is labelled
    
    plt.show()
    # show the graph

main()