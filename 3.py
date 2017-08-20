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
import matplotlib.colors as colors
from matplotlib.ticker import FixedLocator
import pandas as pd
from pandas import DataFrame, Series
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
prep = '3'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

data = init.init_data(courseid, prep)

y_ticks_label = data['y_ticks_label']
heatmap_data = data['heatmap_data']

def draw_3(title, x_label, y_label, y_ticks_label, heatmap_data, output_plot):

    logger.info('Start plotting plot-{} for courseid {}...'.format(prep, courseid))
    weekday_name = ["日", "一", "二", "三", "四", "五", "六"]
    x_ticks_label = [weekday_name[x] for x in xrange(7)]
    x = [(a + 0) for a in xrange(len(x_ticks_label))]
    fig = plt.figure(figsize=(10, 10), dpi=1200)
    y = [ (i) for i in xrange(24)]
    
    zhfont.set_size('x-small')
    plt.subplots_adjust(left=0.25, bottom=0.2, right=None, top=0.8, wspace=None, hspace=None)
    ax = fig.add_subplot(111)
    ax.set_title(title, fontproperties=zhfont, fontsize=16, y=1.05)
    ax.set_xlabel(x_label, fontproperties=zhfont, fontsize=14, labelpad = 10)
    ax.set_ylabel(y_label, fontproperties=zhfont, fontsize=14, labelpad = 14)
    ax.set_xticks(x)
    ax.set_yticks(y)
    #heatmap = ax.pcolor(data, cmap=plt.cm.Blues, norm=colors.LogNorm(vmin=np.amin(data), vmax=np.amax(data)))

    data = collections.OrderedDict(sorted(heatmap_data.items()))
    data = np.array(data.values())
    heatmap = ax.pcolor(data, cmap=plt.cm.Reds, edgecolor='#FF7F50', norm=colors.LogNorm(vmin=np.amin(data), vmax=np.amax(data)))
    #e9967a
    #fig.colorbar(heatmap, ax=ax, extend='max')
    fig.colorbar(heatmap, ax=ax)
    for axis in [ax.xaxis]:
        axis.set(ticks=np.arange(0.5, len(x_ticks_label)))
    #ax.set_xticklabels(x_ticks_label, rotation='-45', minor=False, fontproperties=zhfont)
    ax.set_xticklabels(x_ticks_label, minor=False, fontproperties=zhfont, fontsize=12)
    ax.set_yticklabels(y_ticks_label, va = 'bottom', minor=False)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
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
    #ax.set_yticklabels(y_ticks_label, va = 'center', minor=False)
    #for tick in ax.xaxis.get_majorticklabels():
    #    tick.set_horizontalalignment("left")
    ax.grid(False)

    fig.savefig(output_plot)    
    plt.close(fig)
    logger.info('Done plotting!')
    #end of function draw_A1_01
    

draw_3(u"《国家开放大学学习指南》课程访问量热力图（星期-时段）", u"星期", u"时段", y_ticks_label, heatmap_data, output_plot)


    
