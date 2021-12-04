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

filename="LAB2_Data.txt"
# change this if your filename is different


import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt
import math


data=loadtxt(filename, usecols=(0,1,2,3), skiprows=0, unpack=True)
# load filename, take columns 0 & 1 & 2 & 3, skip 1 row, unpack=transpose x&y

xdata=data[0]
ydata=data[1]
xerror=data[2]
yerror=data[3]
# finished importing data, naming it sensibly

def my_func_lab1(t,a,tau,T,phi):
    return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)

def my_func(theta, T_0, B, C):
    return T_0 + B * theta + C * theta ** 2
# this is the function we want to fit. the first variable must be the
# x-data (time), the rest are the unknown constants we want to determine

init_guess_lab1=(5,80,2,2)
# your initial guess of (a,tau,T,phi)
init_guess=(0.0972, 0.0002, 1.5032)

popt, pcov = optimize.curve_fit(my_func, xdata, ydata, p0=init_guess, maxfev = 1000)
# we have the best fit values in popt[], while pcov[] tells us the uncertainties

# a=popt[0]
# tau=popt[1]
# T=popt[2]
# phi=popt[3]
# # best fit values are named nicely
# u_a=pcov[0,0]**(0.5)
# u_tau=pcov[1,1]**(0.5)
# u_T=pcov[2,2]**(0.5)
# u_phi=pcov[3,3]**(0.5)
# # uncertainties of fit are named nicely
T_0 = popt[0]
B = popt[1]
C = popt[2]
u_T_0 = pcov[0,0]**(0.5)
u_B = pcov[1,1]**(0.5)
u_C = pcov[2,2]**(0.5)

def fitfunction_lab1(t):  
    return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)
#fitfunction(t) gives you your ideal fitted function, i.e. the line of best fit
def fitfunction(theta):
    return T_0 + B * theta + C * theta ** 2

start=min(xdata)
stop=max(xdata)    
xs=np.arange(start,stop,(stop-start)/100000) # fit line has 1000 points
curve=fitfunction(xs)
# (xs,curve) is the line of best fit for the data in (xdata,ydata) 

fig, (ax1,ax2) = plt.subplots(2, 1)
fig.subplots_adjust(hspace=0.6)
#hspace is horizontal space between the graphs

ax1.errorbar(xdata,ydata,yerr=yerror,xerr=xerror,fmt=".")
# plot the data, fmt makes it data points not a line
#ax1.plot(xs,curve, label="Decaying sinusoid best fit line")
ax1.plot(xs, curve, label = "Quadratic best fit line")
ax1.legend()
# plot the best fit curve on top of the data points as a line

#ax1.set_xlabel("Time Elapsed (s)")
ax1.set_xlabel("Release amplitude (rad)")
#ax1.set_ylabel("Angle to Vertical (rad)")
ax1.set_ylabel("Period (s)")
#ax1.set_title("Pendulum String Angle to Vertical vs. Time Elapsed", fontsize=16)
ax1.set_title("Period (s) versus Release Amplitude (rad)")
# HERE is where you change how your graph is labelled

RT = 6
# print("A:", round(a, RT), "+/-", round(u_a, RT))
# print("tau:", round(tau, RT), "+/-", round(u_tau, RT))
# print("T:", round(T, RT), "+/-", round(u_T, RT))
# print("phi:", round(phi, RT), "+/-", round(u_phi, RT))
# Q = math.pi * tau / T
# print("Q:", round(Q, RT), "+/-", round(max(u_tau / tau, 0.0165 / T) * Q, RT))
# prints the various values with uncertainties
print("T_0:", round(T_0, RT), "+/-", round(u_T_0, RT))
print("B:", round(B, RT), "+/-", round(u_B, RT))
print("C:", round(C, RT), "+/-", round(u_C, RT))

residual=ydata-my_func(xdata, T_0, B, C)
# find the residuals
zeroliney=[0,0]
zerolinex=[start,stop]
# create the line y=0

ax2.errorbar(xdata,residual,yerr=yerror,xerr=xerror,fmt=".")
# plot the residuals with error bars
ax2.plot(zerolinex,zeroliney, label="y=0")
ax2.legend()
# plotnthe y=0 line on top

ax2.set_xlabel("Release amplitude")
ax2.set_ylabel("Residuals of Period (s)")
ax2.set_title("Residuals of quadratic fit", fontsize=16)
# HERE is where you change how your graph is labelled

plt.show()
# show the graph