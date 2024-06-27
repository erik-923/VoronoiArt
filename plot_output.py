"""
Erik Blix
This file contains code to read the GAOutput.txt file and create a graph of the progress.
"""

import matplotlib.pyplot as plt
import csv
epoch = []
average = []
best = []
with open('GAoutput.txt', 'r') as datafile:
   plotting = csv.reader(datafile, delimiter=' ')
   for row in plotting:
       epoch.append(float(row[0]))
       average.append(float(row[1]))
       best.append(float(row[2]))
   plt.plot(epoch, average, label="average fitness")
   plt.plot(epoch, best, label="best fitness")
   plt.legend()
   plt.title('Robot Performance over Time')
   plt.xlabel('Epoch')
   plt.ylabel('Fitness')
   plt.show()
