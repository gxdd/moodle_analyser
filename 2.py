# # -*- coding: utf-8 -*-
#!/usr/bin/env python

#---for ipython notebook
#%matplotlib inline
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
import matplotlib.colors as colors

from pandas import DataFrame, Series
import pandas as pd

import datetime as datetime
from datetime import datetime, date, timedelta

import cPickle
import collections

import re

import init

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

courseid = '02970'
prep='2'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

data = init.init_data(courseid, prep)
#x_ticks_label = data1['months']
x_ticks_label = data['x_ticks_label']
y_ticks_label = data['y_ticks_label']
heatmap_data = data['heatmap_data']

def draw_2(title, x_label, y_label, x_ticks_label, y_ticks_label, heatmap_data, output_plot):
    logger.info('Start plotting plot-{} for courseid {}...'.format(prep, courseid))
    x = [(a + 0) for a in xrange(len(x_ticks_label))]
    fig = plt.figure(figsize=(10, 10), dpi=1200)
    y = [ (i) for i in xrange(24)]
    #zhfont = fm.FontProperties(fname='/usr/share/fonts/truetype/arphic/ukai.ttc')
    zhfont.set_size('x-small')
    plt.subplots_adjust(left=0.25, bottom=0.2, right=None, top=0.8, wspace=None, hspace=None)
    ax = fig.add_subplot(111)
    ax.set_title(title, fontproperties=zhfont, fontsize=16, y=1.05)
    ax.set_xlabel(x_label, fontproperties=zhfont, fontsize=14, labelpad = 14)
    ax.set_ylabel(y_label, fontproperties=zhfont, fontsize=14, labelpad = 14)
    ax.set_xticks(x)
    ax.set_yticks(y)
    #ax.set_ylim([0,int(max(y))*(1.1)])  #set_ylim or set_xlim must just adjacent to the bar directive or it will make no effect!
    #ax.bar(x, y, align = 'center', width = 0.7)
    #heatmap = ax.pcolor(data, interpolation='nearest', cmap=plt.cm.coolwarm, alpha=0.8)
    #heatmap = ax.pcolor(data, cmap=plt.cm.coolwarm, alpha=0.8)
    #heatmap = ax.pcolor(data, cmap=plt.cm.coolwarm, alpha=0.8)

    data = collections.OrderedDict(sorted(heatmap_data.items()))
    data = np.array(data.values())
    heatmap = ax.pcolor(data, cmap=plt.cm.Blues, edgecolor='grey', norm=colors.LogNorm(vmin=np.amin(data), vmax=np.amax(data)))
    fig.colorbar(heatmap, ax=ax, extend='max')
    #plt.gca().yaxis.grid(True)
    for axis in [ax.xaxis]:
        axis.set(ticks=np.arange(0.5, len(x_ticks_label)))
    #ax.set_xticklabels(x_ticks_label, rotation='-45', minor=False, fontproperties=zhfont)
    ax.set_xticklabels(x_ticks_label, minor=False, rotation=45, rotation_mode="anchor", fontproperties=zhfont, fontsize=14)
    ax.set_yticklabels(y_ticks_label, va = 'bottom', minor=False)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        pad=10             #x label distance away from x-axis
#        labelbottom='off'  # labels along the bottom edge are off
    )
    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
#        bottom='off',      # ticks along the bottom edge are off
#        top='off',         # ticks along the top edge are off
        left='off',
        right='off',
#        labelbottom='off'  # labels along the bottom edge are off
    )
    #ax.set_xticklabels(x_ticks_label, rotation='45', minor=False)
    #ax.set_yticklabels(y_ticks_label, rotation='180')
    #ax.set_yticklabels(y_ticks_label, va = 'bottom', minor=False)
    ax.grid(False)

    fig.savefig(output_plot)
    plt.close(fig)
    logger.info('Done plotting!')
    #end of function draw_2
    

draw_2(u"《国家开放大学学习指南》课程访问量热力图", u"月份", u"时段", x_ticks_label, y_ticks_label, heatmap_data, output_plot)


    
