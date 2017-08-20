#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append(".")
import os
from os import path

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import dates
from matplotlib.ticker import FixedLocator
import pandas as pd
from pandas import DataFrame, Series
import datetime as datetime
from datetime import datetime, date, timedelta
#import seaborn as sns # improves plot aesthetics
import cPickle
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import re

import init

import logging
import logging.config

logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

courseid = '02970'
prep='7'
output_plot = "./out/{}.pdf".format(prep)
mask_img = './misc/map.png'
data = init.init_data(courseid, prep)

d = path.dirname(__file__)

freqs = data['freqs']['city']

def draw_7(frequencies):
    mask = np.array(Image.open(path.join(d, mask_img)))
    wordcloud = WordCloud(font_path='./msyh.ttf', stopwords=set(),background_color="white", max_words=2000, mask=mask, relative_scaling=.2, max_font_size=1000).generate_from_frequencies(frequencies)
    logger.info('Start plotting plot-{} for courseid {}...'.format(prep, courseid))
    fig = plt.figure(figsize=(12, 12), dpi=600)
    ax = fig.add_subplot(111)
    plt.axis("off")
    ax.imshow(wordcloud)
    plt.figure()
    fig.savefig(output_plot)
    plt.close(fig)
    logger.info('Done plotting!')

draw_7(freqs)
