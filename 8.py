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
import seaborn as sns # improves plot aesthetics
import cPickle

import re
import math

import init

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

courseid_list = ('02969', '02970')
prep = '8'
output_plot = "./out/{}.pdf".format(prep)
zhfont = mpl.font_manager.FontProperties(fname=init.font_lib['华文仿宋'])

data = [init.init_data(cid, prep) for cid in courseid_list]
radar_raw_data = [x['metrics'] for x in data]


def radar_transform_raw_data(raw_data, labels):

    data = np.zeros_like(raw_data)

    
    for i, r in enumerate(raw_data):
        data[i][0] = format(r[0]*5, '.2f')
        data[i][1] = format(r[1]*5/float(labels[1][-1]), '.2f')
        data[i][2] = format(r[2]*5/float(labels[2][-1]), '.2f')
        data[i][3] = format(r[3]*5/float(labels[3][-1]), '.2f')
        data[i][4] = format(r[4]*5/float(labels[4][-1]), '.2f')
        data[i][5] = format(r[5]*5, '.2f')
    
        
    return data


def gen_label_marks(raw_data):
    #用户活跃度刻度
    labels = [['20', '40', '60', '80', '100'],]
    label_ranges = zip(*raw_data)
    #人均在线时长刻度
    l = label_ranges[1]
    l_max = math.ceil(max(l))//4
    l_max = (l_max+1)*4 if l_max > 1 else 1
    l_min = (math.floor(min(l))//4)*4 if l_max >1 else 0
    if l_max == 1:
        labels.append(['0', '0.25', '0.5', '0.75', '1'])
    else:
        labels.append(list(np.linspace(l_min, l_max, 5).astype(int).astype(str))) 
    #人均论坛访问量刻度                                         
    l = label_ranges[2]
    l_max = math.ceil(max(l))//4
    l_max = (l_max+1)*4 if l_max > 1 else 1
    l_min = (math.floor(min(l))//4)*4 if l_max >1 else 0
    if l_max == 1:
        labels.append(['0', '0.25', '0.5', '0.75', '1'])
    else:
        labels.append(list(np.linspace(l_min, l_max, 5).astype(int).astype(str)))
                                                            
    #论坛贴数刻度                                             
    l = label_ranges[3]
    l_max = math.ceil(max(l))//4
    l_max = (l_max+1)*4 if l_max > 1 else 1
    l_min = (math.floor(min(l))//4)*4 if l_max >1 else 0
    if l_max == 1:
        labels.append(['0', '0.25', '0.5', '0.75', '1'])
    else:
        labels.append(list(np.linspace(l_min, l_max, 5).astype(int).astype(str)))                                                             
    #论坛回复率                                              
    l = label_ranges[4]
    l_max = math.ceil(max(l))//4
    l_max = (l_max+1)*4 if l_max > 1 else 1
    l_min = (math.floor(min(l))//4)*4 if l_max >1 else 0
    if l_max == 1:
        labels.append(['0', '0.25', '0.5', '0.75', '1'])
    else:
        labels.append(list(np.linspace(l_min, l_max, 5).astype(int).astype(str)))
    #labels.append(['1', '2', '3', '4', '5'])
 
    #论坛生命力
    labels.append(labels[0])
 
    return labels


def plot_radar(fig, plot_title, titles, labels, data, output, rect=None):
    
    if rect is None:
        rect = [0., 0., 0.65, 0.65]
    n = len(titles)
    
    angles = [a if a <=360. else a - 360. for a in np.arange(90, 90+360, 360.0/n)]

    axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) for i in range(n)]

    ax1 = axes[0]

    l, text = ax1.set_thetagrids(angles, labels=titles, fontproperties=zhfont, fontsize=14)

    #[txt.set_rotation(angle-90) for txt, angle in zip(text, self.angles)]
    text[1].set_rotation(angles[1]-90)
    text[2].set_rotation(angles[2]+90)
    text[4].set_rotation(angles[4]+90)
    text[5].set_rotation(angles[5]-90)
 
    ax1.set_title(plot_title, fontproperties=zhfont, fontsize=18, y=1.2)
    #obsoleted!
    #ax1.set_axis_bgcolor("#F2F2F2") 
    ax1.set_facecolor("#F2F2F2")
    for ax in axes[1:]:
        ax.patch.set_visible(False)
        ax.grid("off")
        ax.xaxis.set_visible(False)
 
    for ax, angle, label in zip(axes, angles, labels):
 
        
        ax.set_rgrids(range(1, 6), angle=angle, labels=label)
        ax.spines["polar"].set_visible(False)
        #ax.patch.set_facecolor('Azure')
        #ax.patch.set_alpha(0.8)
        
        ax.set_ylim(0, 5.5)
        ax.xaxis.grid(True,color='black',linestyle='-', lw=2, alpha=0.2)
        #pos=ax.get_rlabel_position()
        #ax.set_rlabel_position(pos+4)
        
    def plot(values, *args, **kw):
        
        
        angle = np.deg2rad(np.r_[angles, angles[0]])
        values = np.r_[values, values[0]]
        ax1.plot(angle, values, *args, **kw)
        
#
    def fill(values, *args, **kw):
        
        
        angle = np.deg2rad(np.r_[angles, angles[0]])
        values = np.r_[values, values[0]]
        ax1.fill(angle, values, *args, **kw)
 
    def legend(*args, **kw):
        h, l = ax1.get_legend_handles_labels()
        #self.ax.legend(h, l,loc='center left', bbox_to_anchor=(0.72, 0.8), prop=self.font, fontsize=8, labelspacing=0.3)
        #legend do not have the fontsize attribute!!! if you set prop={'size':16} , you will end up with funny characters when display chinese!! see my evernotes: "python matplotlib中文显示乱码解决 - Linux系统教程"
        ax1.legend(h[2:], l[2:],loc='center left', bbox_to_anchor=(0.76, 1), prop=zhfont, labelspacing=0.3)


    plot(data[0], "-", lw=2, color="#20B2AA", alpha=0.4, label="中国特色社会主义体系概论")
    plot(data[1], "-", lw=2, color="#FFA500", alpha=0.4, label="国家开放大学学习指南")
    fill(data[0], "-", lw=2, color="#20B2AA", alpha=0.4, label="中国特色社会主义体系概论")
    fill(data[1], "-", lw=2, color="#FFA500", alpha=0.4, label="国家开放大学学习指南")
     
    legend()
    
    fig.savefig(output, bbox_inches='tight', pad_inches = 1)
    
    plt.close(fig)
    
    
def draw_8(raw_data, output_plot):

    labels = gen_label_marks(raw_data)
    radar_data = radar_transform_raw_data(raw_data, labels)
     
    fig = plt.figure(figsize=(10, 8), dpi=1200)
     
    plot_title = '课程健康度对比雷达图'    
    titles = ['用户\n活跃度(%)', '人均在线\n时长(秒)', '人均论坛\n访问量(次)', '论坛\n贴数(个)',  '论坛\n回复率(*100%)', '论坛\n生命力(%)' ]

    logger.info('Start plotting plot-{} for courses...'.format(prep))
    
    plot_radar(fig, plot_title, titles, labels, radar_data, output_plot)
    
    logger.info('Done plotting!')


draw_8(radar_raw_data, output_plot)
