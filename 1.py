# # -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(".")
import os

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import dates
from matplotlib.ticker import FixedLocator
from pandas import DataFrame, Series
import pandas as pd
import datetime as datetime
from datetime import datetime, date, timedelta
import cPickle

import re

import init

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

prep = '1'
output_plot = "./out/1.pdf"
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])
courseid = '02970'

data = init.init_data(courseid, prep)

x_ticks_label = data['monthly']
y = data['visits']

def draw_1(title, x_label, y_label, x_ticks_label, y, output_plot):

    logger.info('Printing plot_{} for courseid: {}...'.format(prep, courseid))
    x = [(a + 1) for a in xrange(len(y))]
    fig = plt.figure(figsize=(10, 8), dpi=200)
    
    plt.subplots_adjust(left=None, bottom=0.15, right=None, top=0.85, wspace=None, hspace=0.1)
    ax = fig.add_subplot(111)
    ax.set_title(title, fontproperties=zhfont, fontsize=16, y=1.05)
    ax.set_xlabel(x_label, fontproperties=zhfont, fontsize=12)
    ax.set_ylabel(y_label, fontproperties=zhfont, fontsize=12)
    #print int(max(y))
    
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(x)
    ax.set_yscale('log')
    ax.set_xlim([0,len(x)+1])
    ax.set_ylim([1,int(max(y))*(1.6)])  #left boundary of ylim must be 1 when using log!!
    #ax.bar(x, y,align = 'center', width = 0.7, log=True)
    #ax.bar(x, y,align = 'center', width = 0.8, color='#3366FF', alpha = 0.8, edgecolor='w', log=True)
    ax.bar(x, y, align = 'center', width = 0.8, color='#3366FF', alpha = 0.8, edgecolor='w')
    #ax.bar(x, y,log = True,  align = 'center', width = 0.7)
    #plt.gca().yaxis.grid(True)
    ax.set_xticklabels(x_ticks_label, rotation=45, ha="center", fontsize=12)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        pad=5,             #x label distance away from x-axis
        labelsize=10
#        labelbottom='off'  # labels along the bottom edge are off
    )
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    #ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    #ax.xaxis.set_tick_params(width=1)
    rects = ax.patches

    for rect, label in zip(rects, y):

        height = rect.get_height()
        if height == 0:
            height = 1.05
        else:
            height = height*1.05
            
        ax.text(rect.get_x() + rect.get_width()/2, height, int(label), ha='center', va='bottom')

    fig.savefig(output_plot)
    plt.close(fig)
    logger.info('Done plotting!')
    #end of function draw_1


draw_1(u"《国家开放大学学习指南》课程月访问量统计", u"月份", u"访问次数", x_ticks_label, y, output_plot)

