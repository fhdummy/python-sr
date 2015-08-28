#!/usr/bin/python

'''
Author:	Stefan Binna
Date:	26.08.15
Detail: Takes the file .\data.csv and generates a boxplot.
		The first two lines of the file are skipped, 
		so make sure that the actual value lines start at line 3.
'''

from pylab import *
import matplotlib.pyplot as plt
import numpy as np

# Get data from file (3 rows, delimited by spaces), skip first two lines
data = np.genfromtxt('.\data_boxplot.csv', delimiter='', names=['x', 'y', 'z'], skip_header=2)

# Calculate the delay
time = (data['z'] - data['x']) / 1000

# Plot lost packets
figure(num=None, figsize=(15, 10), dpi=96)
plt.boxplot(data['y'])
plt.title('Boxplot lost packets')
plt.ylabel('lost packets')
plt.annotate('Median: %s'%np.median(data['y']), xy=(0, 1), xycoords='axes fraction', fontsize=16, xytext=(0.05, 0.9))

# Plot delay
figure(num=None, figsize=(15, 10), dpi=96)
plt.boxplot(time)
plt.title('Boxplot fast failover time')
plt.ylabel('time / ms')
plt.annotate('Median: %s'%np.median(time), xy=(0, 1), xycoords='axes fraction', fontsize=16, xytext=(0.05, 0.9))

plt.show()



