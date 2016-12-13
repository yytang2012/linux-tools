#!/usr/bin/env python3
# coding=utf-8

import matplotlib.pyplot as plt
import numpy as np

n = 3
ind = np.arange(n)
width = 0.27
pre_width = 0.1
fig = plt.figure()
ax = fig.add_subplot(111)
print(ind+pre_width)
yvals = [4, 9, 2]
rects1 = ax.bar(pre_width+ind, yvals, width, color='r')
zvals = [1,2,3]
rects2 = ax.bar(pre_width+ind+width, zvals, width, color='g')
kvals = [11,12,13]
rects3 = ax.bar(pre_width+ind+width*2, kvals, width, color='b')

ax.set_ylabel('Scores')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('2011-Jan-4', '2011-Jan-5', '2011-Jan-6') )
ax.legend( (rects1[0], rects2[0], rects3[0]), ('y', 'z', 'k') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.show()


