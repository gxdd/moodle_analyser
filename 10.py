
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

prep = '10'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

courseid_list = ('02970', '02969', '50421')
coursename_list = ('国家开放大学学习指南', '中国特色社会主义体系概论', '教师口语')

data = [init.init_data(cid, prep) for cid in courseid_list]

left_offset = min([x['left_offset'] for x in data])
start_date = min([x['start_date'] for x in data]).strftime('%Y-%m-%d')

end_date = max([x['end_date'] for x in data]).strftime('%Y-%m-%d')

new_ix = pd.DatetimeIndex(start = start_date, end = end_date, freq='D')
sliced_online_stats = [x['online_stats'].reindex(new_ix).fillna(0) for x in data]

avg_online_time = [x['avg_online_time'] for x in sliced_online_stats]
users_cnt = [x['users'] for x in sliced_online_stats]
months = pd.date_range(*(pd.to_datetime([start_date, end_date]) + pd.offsets.MonthEnd()), freq='M').strftime('%Y-%m')


def draw_10(title, x_label, y_label, x_ticks_label, coursename_list, avg_online_time, users_cnt, left_offset, output_plot):

    logger.info('Start plotting plot-{} for courses...'.format(prep))

    x = [a+left_offset for a in xrange(len(avg_online_time[0]))]
    fig = plt.figure(figsize=(12, 7.5), dpi=1200)
    
    zhfont.set_size('small')
    plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.8, wspace=None, hspace=0.1)
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2,sharex=ax1)
    def set_ax(ax, ylabel):
        ax.yaxis.set_ticks_position('left')   
        ax.xaxis.set_ticks_position('bottom')
        
        last_tick = datetime.strptime(x_ticks_label[0]+'-01', '%Y-%m-%d')
        major_index = [0,]
        for i in x_ticks_label[1:]:
            first_day_of_month = datetime.strptime(i+'-01', '%Y-%m-%d')
            month_days_span = (first_day_of_month - last_tick).days
            major_index.append(major_index[-1] + month_days_span)
            last_tick = first_day_of_month
        
        ax.set_xlim([0, major_index[-1]])
        #ax.set_xticks(x_ticks)
        majorLocator   = FixedLocator(major_index)
        minorLocator   = FixedLocator(np.linspace(0, major_index[-1], len(x)))
        ax.xaxis.set_major_locator(majorLocator)
        ax.xaxis.set_minor_locator(minorLocator)

        ax.tick_params(axis = 'x', length=5, which='major')
        ax.tick_params(axis = 'x', which='both', direction='out', pad=2)
        ax.grid(True)
        ax.set_ylabel(ylabel, fontproperties=zhfont, fontsize=12, labelpad = 15)
    

    plt.setp(ax1.get_xticklabels(), visible=False)
    set_ax(ax1, y_label[0])
    set_ax(ax2, y_label[1])
    #ax1.set_yscale("symlog",basex=2)
    ax2.set_xlabel(x_label, fontproperties=zhfont, fontsize=12)
    ax2.set_ylim([0,int(max([max(e) for e in users_cnt]))*(1.05)])
    #ax2.set_xlabel(x_label, fontproperties=zhfont, fontsize=16)
    ax2.set_xticklabels(x_ticks_label, rotation='0', fontproperties=zhfont)
    ax2.tick_params(axis='x', which='major', labelsize=12)

    colors = ['#0000CC', '#EEEE00', '#99FF00', '#FF0000', '#FF00FF']

    for i, c in enumerate(coursename_list):
        
        ax1.fill_between(x, 0, avg_online_time[i], color=colors[i], alpha =0.6, lw=0.5, label = c, zorder=len(colors)-i)
        ax2.plot(x, users_cnt[i], '-',color = colors[i], alpha = 0.8, lw=0.8, label = c)  
    

    h1, l1 = ax1.get_legend_handles_labels()
    ax1.legend(h1, l1,loc='center', bbox_to_anchor=(0.5, 1.1), prop=zhfont, ncol=5, frameon=True)
    
    ax1.set_title(title, fontproperties=zhfont, fontsize=16, y=1.2)
    fig.savefig(output_plot)
    plt.close(fig)
    logger.info('Done plotting!')

    
draw_10(u"2016春季学期课程在线情况对比图", u"日期", [u"人均在线时间（分钟）", u"在线人数"], months, coursename_list, avg_online_time, users_cnt, left_offset, output_plot)
