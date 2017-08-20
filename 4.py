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
import matplotlib.colors as colors
import pandas as pd
from pandas import DataFrame, Series
import datetime as datetime
from datetime import datetime, date, timedelta
import cPickle
import re
import collections
from random import shuffle, sample

import init

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

courseid = '02970'
prep = '4'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

data = init.init_data(courseid, prep)

def draw_4(title, data, output_plot):
    logger.info('Start plotting plot-{} for courseid {}...'.format(prep, courseid))
    legend_label = data['legend_label']
    slices = data['slices']
    total_users = data['total_users']
    fig = plt.figure(figsize=(10, 8), dpi=1200)
    
#    percents = ['访问数在{}之间用户数占比'.format(x) for x in XXX]
    plt.subplots_adjust(left=None, bottom=0.2, right=None, top=0.9, wspace=None, hspace=None)
    ax = fig.add_subplot(111)

    cmap = plt.cm.Spectral

    colors = np.linspace(0., 1., len(slices))
    shuffle(colors)
    #colors = sample(colors, len(slices))
    colors = cmap(colors)
    ax.set_title(title, fontproperties=zhfont, fontsize=16)
    plt.axis('equal')

    #percent = [100.0*i/sum(slices) for i in slices]

    patches, texts = plt.pie(slices, colors=colors, startangle=0, radius=1.2)
    #labels = ['{0} - {1:1.2f} %'.format(i,j) for i, j in zip(legend_label, percent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, legend_label, slices), key=lambda x: x[2], reverse=True))

    #pie_wedge_collection = ax.pie(slices, colors=colors, labels=labels, labeldistance=1.05);

    for p in patches:
        p.set_edgecolor('white')

    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(0.1, .7), prop=zhfont, fontsize=14)

    #plt.text(0,0,u'课程平台用户总数：{}'.format(total_users),fontproperties=zhfont, horizontalalignment='center', backgroundcolor='palegreen', bbox=dict(boxstyle="round", facecolor='#D8D8D8', ec="0.5", pad=0.5, alpha=1), fontweight='bold')
    plt.text(0,0,u'课程平台用户总数：{}'.format(total_users),fontproperties=zhfont, horizontalalignment='center', backgroundcolor='palegreen', fontweight='bold')

    fig.savefig(output_plot)
    
    plt.close(fig)
    logger.info('Done plotting!')
    #end of function draw_4
    
    
draw_4(u"《国家开放大学学习指南》课程用户访问数分级统计", data, output_plot)
    
