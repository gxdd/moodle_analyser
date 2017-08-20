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
import datetime as datetime
from datetime import datetime, date, timedelta
import pandas as pd
from pandas import DataFrame, Series
#import seaborn as sns # improves plot aesthetics
import cPickle

import re

import init

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

courseid = '02970'
prep = '9'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

data = init.init_data(courseid, prep)

def draw_9(title, x_label, y_label, data, output_plot):
    logger.info('Start plotting plot-{} for courseid {}...'.format(prep, courseid))
    x = [a+data['left_offset'] for a in xrange(len(data['forum']))]
    fig = plt.figure(figsize=(10, 8), dpi=1200)
    
    plt.subplots_adjust(left=None, bottom=0.15, right=None, top=0.85, wspace=None, hspace=None)
    ax = fig.add_subplot(111)
    
    ax.yaxis.set_ticks_position('left')   
    ax.xaxis.set_ticks_position('bottom')
    last_tick = datetime.strptime(data['x_ticks_label'][0]+'-01', '%Y-%m-%d')
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
    #ax.tick_params(axis = 'x', length=5, which='major', labelsize=16)
    ax.tick_params(axis = 'x', length=5, which='major')
    ax.tick_params(axis = 'x', which='both', direction='out', pad=2)
    #ax.set_xticklabels(x_ticks_label, rotation='30', fontproperties=zhfont)
    ax.set_xticklabels(data['x_ticks_label'], rotation='0', fontproperties=zhfont)
    ax.tick_params(axis='x', which='major', labelsize=12)
    #ax.set_xticklabels(x_ticks_label, rotation='vertical', fontproperties=zhfont)
    ax.set_title(title, fontproperties=zhfont, fontsize=16, y=1.02)
    ax.set_xlabel(x_label, fontproperties=zhfont, fontsize=14)
    ax.set_ylabel(y_label, fontproperties=zhfont, fontsize=14, labelpad = 14)
    #ax.get_xaxis().set_tick_params(direction='out', which='both')
#    plt.semilogy(x, total, '.-',color='#87ceeb', alpha =0.9, lw=1.5) 
#    plt.semilogy(x, forum, '.-', color='#cd3278', alpha = 0.9, lw=0.8)  
#    plt.semilogy(x, course, '.-', color='#e9967a', alpha = 0.9, lw=0.8)
#    plt.semilogy(x, page, '.-',color='#e7ceeb', alpha =0.9, lw=0.8) 
#    plt.semilogy(x,quiz, '.-', color='#ed3278', alpha = 0.9, lw=0.8)  
#    plt.semilogy(x,others, '.-', color='#f9967a', alpha = 0.9, lw=0.8)

    ax.plot(x, data['forum'], '.-',color='#D15FEE', alpha = 0.8, lw=0.8, label='论坛')  
    ax.plot(x, data['course'], '.-', color='#EEEE00', alpha = 0.8, lw=0.8, label='课程')
    ax.plot(x, data['page'], '.-',color='#33CCCC', alpha =0.8, lw=0.8, label='资源') 
    ax.plot(x,data['quiz'], '.-',color='#0033CC', alpha = 0.8, lw=0.8, label='测验')  
    ax.plot(x,data['others'], '.-',color='#FF6633', alpha = 0.8, lw=0.8, label='其他')
    ax.fill_between(x, 0, data['total'], color='#eeaeee', alpha =0.5, lw=0.5, label='总体')

    h, l = ax.get_legend_handles_labels()
    ax.legend(h, l,loc='center left', bbox_to_anchor=(0.8, 0.8), prop=zhfont, fontsize=14)

    fig.savefig(output_plot)
    plt.close(fig)
    logger.info('Done plotting!')
    #end of function draw_9

draw_9(u"《国家开放大学学习指南》课程各模块人均在线时长统计图", u"日期", u"人均在线时间（分钟）", data, output_plot)
