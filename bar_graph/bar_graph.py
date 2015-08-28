#!/usr/bin/python

'''
Author:	Stefan Binna
Date:	26.08.15
Detail: Takes the file .\data.csv and generates a bar graph.
		The blue bars indicate lost packets at the event 'Disconnect', the red bars
		indicate lost packets at the event 'Connect' and the green bars indicate lost packets
		at the event 'Unknown'
		Make sure, that the Start-Timestamp of the very first packet is located in line 1.
		Make sure that the actual value lines start at line 3.
'''

from pylab import *
import pylab
import matplotlib.pyplot as plt
import numpy as np

# Set global configuration parameters
period = 10L	# seconds, interval between disconnect and connect
startDelay = 20L	# seconds, time for the first event after start of measurement
tolerance = 4L	# +/- seconds, how much tolerance is allowed that a packet still counts to an event
variance = 4L	# -/+ seconds, events that are very close together get added up, it they are in the defined variance
endTime = 600L	# seconds, total time of measurement

# Adapt the unit(s) so that the value is in microseconds
period *= 1000000
startDelay *= 1000000
tolerance *= 1000000
variance *= 1000000
endTime *= 1000000

# Get starttimestamp
f = open('.\data_bar.csv', 'r')
start = f.readline()
f.close()

# Calculate the end time
endTime += long(start)

# Get data from file (3 rows, delimited by spaces)
data = np.genfromtxt('.\data_bar.csv', delimiter='', names=['x', 'y', 'z'], skip_header=2).tolist()
dataCopy = []
dataCopy += data

# Calculate the disconnect stamps
disconnectStamps = []
stampsForBoxplot = []   # These stamps are then used to generate the data for the boxplot, it's just a copy of disconnectStamps

# Create an exact copy of data. With help of this copy I can iterate through the copy and modify elements of the original
# data.
dataIterateHelper = []
dataIterateHelper += data

currentTime = long(start) + startDelay

while currentTime <= endTime:
	for val1 in dataIterateHelper:
		if val1[0] > (currentTime - tolerance) and val1[0] < (currentTime + tolerance):
			disconnectStamps.append(val1)
			data.remove(val1)   #Remove them, because they are already saved in disconnectStamps
			# print('{0:.0f}'.format(val[0]))

	currentTime+=((period*2))

stampsForBoxplot += disconnectStamps    # Used for the boxplot generation afterwards

# Calculate the connect stamps
connectStamps = []
currentTime = long(start) + startDelay + period

while currentTime <= endTime:
	for val2 in dataIterateHelper:
		if val2[0] > (currentTime - tolerance) and val2[0] < (currentTime + tolerance):
			connectStamps.append(val2)
			data.remove(val2)   #Remove them, because they are already saved in connectStamps

	currentTime+=((period*2))

# Merge timestamps, that are within the variance, to one timestamp. Keep the starttime of the first timestamp that is
# in variance and sum the values of lost_packets of all the timestamps in variance.
# This is made for disconnectStamps
tempStamp = []	# Holds value(s) of lost_packets of all timestamps in variance
tempStarttime = []	# Value(s) of starttime
tempEndtime = []	# Value(s) of endtime

# Perm... is the temporary array for saving all the merged timestamps
permStamp = []
permStarttime = []
permEndtime = []

stamp = 0   # Holds the temporary summed stamp values
flag = 0

# Create an exact copy of disconnectStamps. With help of this copy I can iterate through the copy and modify elements of the original
# disconnectStamps.
disconnectStampsIterateHelper = []
disconnectStampsIterateHelper += disconnectStamps

currentTime = long(start) + startDelay	# The currentTime to start with is the initial start time plus the start delay

while currentTime <= endTime:
	for val3 in disconnectStampsIterateHelper:
		if val3[0] > (currentTime - variance) and val3[0] < (currentTime + variance):	# If starttimestamp of timestamp is
																						# in variance
			tempStarttime.append(val3[0])
			tempStamp.append(val3[1])
			tempEndtime.append(val3[2])
			disconnectStamps.remove(val3)
			flag = 1

		else:
			if flag == 1:
				permStarttime.append(tempStarttime[0])
				for temp in tempStamp:
					stamp += temp

				permStamp.append(stamp)
				permEndtime.append(tempEndtime[0])
				tempStamp = []
				tempStarttime = []
				tempEndtime = []
				stamp = 0
				flag = 0
				continue

	currentTime += period

disconnectStampsMerged = []
disconnectStampsMerged = zip(permStarttime, permStamp, permEndtime)	# Combine all the merged timestamps to one big array

# Merge timestamps, that are within the variance, to one timestamp. Keep the starttime of the first timestamp that is
# in variance and sum the values of lost_packets of all the timestamps in variance.
# This is made for the connectStamps
tempStamp = []  # Holds value(s) of lost_packets of all timestamps in variance
tempStarttime = []  # Value(s) of starttime
tempEndtime = []    # Value(s) of endtime

# Perm... is the temporary array for saving all the merged timestamps
permStamp = []
permStarttime = []
permEndtime = []

stamp = 0   # Holds the temporary summed stamp values
flag = 0

# Create an exact copy of connectStamps. With help of this copy I can iterate through the copy and modify elements of the original
# connectStamps.
connectStampsIterateHelper = []
connectStampsIterateHelper += connectStamps

currentTime = long(start) + startDelay	# The currentTime to start with is the initial start time plus the start delay

while currentTime <= endTime:
	for val4 in connectStampsIterateHelper:
		if val4[0] > (currentTime - variance) and val4[0] < (currentTime + variance):	# If starttimestamp of timestamp is
																						# in variance
			tempStarttime.append(val4[0])
			tempStamp.append(val4[1])
			tempEndtime.append(val4[2])
			connectStamps.remove(val4)
			flag = 1
		else:
			if flag == 1:
				permStarttime.append(tempStarttime[0])
				for temp in tempStamp:
					stamp += temp

				permStamp.append(stamp)
				permEndtime.append(tempEndtime[0])
				tempStamp = []
				tempStarttime = []
				tempEndtime = []
				stamp = 0
				flag = 0
				continue

	currentTime += period

connectStampsMerged = []
connectStampsMerged = zip(permStarttime, permStamp, permEndtime)    # Combine all the merged timestamps to one big array

# Look for entries that are out of tolerance and out of variance.
# Therefore data can be used, because everything that is out of tolerance and therefore variance has been already
# deleted out of the data list.
noEventPackets = []
noEventPackets += data

# Draw the graph
f, ax = plt.subplots(num=None, figsize=(15, 10), dpi=96)

width = 2.5 # Width of the drawn bars

connectStamp = []
connectTime = []
disconnectStamp = []
disconnectTime = []
noEventPacketsStamp =[]
noEventPacketsTime = []
minmaxListStamp = []
minmaxListTime = []

# Add all connectStamps and disconnectStamp together.
# Because for example there are two lists that contain connectStamps: connectStampsMerged and connectStamps.
# In order to be able to display all, they have to be 'merged'.
if connectStampsMerged:
	connectStamp += [row[1] for row in connectStampsMerged]
	connectTime += [row[0] for row in connectStampsMerged]
	minmaxListStamp += [row[1] for row in connectStampsMerged]
	minmaxListTime += [row[0] for row in connectStampsMerged]
if connectStamps:
	connectStamp += [row[1] for row in connectStamps]
	connectTime += [row[0] for row in connectStamps]
	minmaxListStamp += [row[1] for row in connectStamps]
	minmaxListTime += [row[0] for row in connectStamps]

if disconnectStampsMerged:
	disconnectStamp += [row[1] for row in disconnectStampsMerged]
	disconnectTime += [row[0] for row in disconnectStampsMerged]
	minmaxListStamp += [row[1] for row in disconnectStampsMerged]
	minmaxListTime += [row[0] for row in disconnectStampsMerged]
if disconnectStamps:
	disconnectStamp += [row[1] for row in disconnectStamps]
	disconnectTime += [row[0] for row in disconnectStamps]
	minmaxListStamp += [row[1] for row in disconnectStamps]
	minmaxListTime += [row[0] for row in disconnectStamps]

if noEventPackets:
	noEventPacketsTime = [row[0] for row in noEventPackets]
	noEventPacketsStamp = [row[1] for row in noEventPackets]
	minmaxListStamp += [row[1] for row in noEventPackets]
	minmaxListTime += [row[0] for row in noEventPackets]

# Scale all timestamps to seconds for better visability
connectTimeIterator = []
connectTimeIterator += connectTime
connectTimeScaled = []
for temp in connectTimeIterator:
	connectTimeScaled.append((temp - float(start)) / 1000000)

disconnectTimeIterator = []
disconnectTimeIterator += disconnectTime
disconnectTimeScaled = []
for temp in disconnectTimeIterator:
	disconnectTimeScaled.append((temp - float(start)) / 1000000)

noEventPacketsTimeIterator = []
noEventPacketsTimeIterator += noEventPacketsTime
noEventPacketsTimeScaled = []
for temp in noEventPacketsTimeIterator:
	noEventPacketsTimeScaled.append((temp - float(start)) / 1000000)

# Print the bars
plt.bar(connectTimeScaled, connectStamp, width, color='red', align='center', label='Connect Event')
plt.bar(disconnectTimeScaled, disconnectStamp, width, color='blue', align='center', label='Disconnect Event')
plt.bar(noEventPacketsTimeScaled, noEventPacketsStamp, width, color='green', align='center', label='Unknown Event')

# legend = plt.legend(loc='upper right', fontsize='x-large')  # Draw the legend

# Set the x and y axes ranges
minmaxListTime = sorted(minmaxListTime) # Sort the list
minmaxListTimeIterator = []
minmaxListTimeIterator += minmaxListTime
minmaxListTimeScaled = []
for temp in minmaxListTimeIterator:
	minmaxListTimeScaled.append((temp - float(start)) / 1000000)

pylab.xlim([0, max(minmaxListTimeScaled) + (width * 4)])
pylab.ylim([0, max(minmaxListStamp) + max(minmaxListStamp)/50])

ax.xaxis.set_major_locator(MultipleLocator(50)) # Sets the x axis scale

# Set the labels
# label = []
# for temp in minmaxListTime:
	# label.append('{0:.0f}'.format(temp))
# plt.xticks(minmaxListTime, label, rotation='vertical')

# Set axe labels
plt.xlabel('Unix timestamp / seconds')
plt.ylabel('Lost packets / 1 packet')

# Make room for the labels
plt.tight_layout()

# Write disconnect timestamps to the file used by boxplot
file2 = open('../boxplot/data_boxplot.csv', 'w')
for item in stampsForBoxplot:
	file2.write('%s    ' %str(item[0]))
	file2.write('%s    ' %str(item[1]))
	file2.write('%s\n' %str(item[2]))
file2.close()

# Show the figure
plt.show()