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
import pandas as pd
from pandas import DataFrame, Series
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

courseid = '02970'
prep = '6'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

data = init.init_data(courseid, prep)

def draw_6(title, x_label, y_label, data, filename):

    logger.info('Start plotting plot-{} for courseid {}...'.format(prep, courseid))
    #x = [a for a in xrange(len(S1))]
    x = [a+data['left_offset'] for a in xrange(len(data['s1']))]

    fig = plt.figure(figsize=(10, 8), dpi=1200)
    
    plt.subplots_adjust(left=0.15, bottom=0.15, right=None, top=0.85, wspace=None, hspace=None)
    ax = fig.add_subplot(111)
    
    ax.yaxis.set_ticks_position('left')   
    ax.xaxis.set_ticks_position('bottom')


    last_tick = datetime.strptime(data['months'][0]+'-01', '%Y-%m-%d')
    major_index = [0,]

    for i in data['x_ticks_label'][1:]:
        first_day_of_month = datetime.strptime(i+'-01', '%Y-%m-%d')
        month_days_span = (first_day_of_month - last_tick).days
        major_index.append(major_index[-1] + month_days_span)
        last_tick = first_day_of_month
        
    ax.set_xlim([0, major_index[-1]])

    majorLocator   = FixedLocator(major_index)
    minorLocator   = FixedLocator(np.linspace(0, major_index[-1], len(x)))
    
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.set_xticklabels(data['x_ticks_label'], rotation='vertical', fontproperties=zhfont, fontsize=16)
    ax.set_title(title, fontproperties=zhfont, fontsize=16, y=1.05)
    ax.set_xlabel(x_label, fontproperties=zhfont, fontsize=14, labelpad=14)
    ax.set_ylabel(y_label, fontproperties=zhfont, fontsize=14, labelpad=14)
    
    plt.semilogy(x, data['s1'], '.-', label = '沉睡用户数', color='#87ceeb', alpha =0.9, lw=0.8) 
    plt.semilogy(x, data['s2'], '.-', label = '活跃用户数', color='#cd3278', alpha = 0.9, lw=0.8)  
    plt.semilogy(x, data['s3'], '.-', label = '新增用户数', color='#e9967a', alpha = 0.9, lw=0.8)
    #plt.legend(legend_label, loc='center left', bbox_to_anchor=(0.75, 0.7), prop=zhfont, fontsize=8)
    h, l = ax.get_legend_handles_labels()
    ax.legend(h, l,loc='center left', bbox_to_anchor=(0.75, 0.8), prop=zhfont, fontsize=12)
    
    fig.savefig(output_plot)
    plt.close(fig)
    logger.info('Done plotting!')


draw_6(u"《国家开放大学学习指南》课程用户活跃情况统计图", u"日期", u"用户数", data, output_plot)
    
