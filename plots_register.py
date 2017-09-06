# # -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import numpy as np
import matplotlib as mpl
import pandas as pd
from datetime import datetime, timedelta

import socket
from struct import pack, unpack
from random import uniform
import time
#import requests
import json
import re

import init

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

def prep_1(data):

    #using data['logs']
    df = pd.DataFrame(data['logs']['visit'].values, index=data['logs']['time']).resample('MS', closed='left').sum()
    df = df.fillna(0.0).astype(int)
    df = df.reset_index()
    monthly = df['time'].apply(lambda x: x.strftime('%Y-%m')).tolist()
    p1 = {
        'monthly': monthly,
        'visits': list(df[0])
    }

    return p1

def prep_2(data):

    #using data['month_span_list'], data['time_table'], data['month_span_str']
           
    #initialize
    heatmap_data = {key : [] for key in ['%02d:00-%02d:00' % (h, h+1) for h in xrange(24)]}
    #data['month']
    heatmap_data['23:00-23:59'] = heatmap_data.pop('23:00-24:00')

    #month_span_list add an extra month comparing to month_span_str
    calender = data['month_span_list'][:-1]

    hours = sorted(heatmap_data.keys())

    for hour in hours:
        start_hour, end_hour = hour.split('-')
        start_hour = datetime.strptime(start_hour, '%H:%M').time()
        end_hour = datetime.strptime(end_hour, '%H:%M').time()
        for c in calender:
            #heatmap_data[hour].append(max(1,int(data['time_table'].loc[c[0], c[1]].sum(level='time(24h)').loc[start_hour:end_hour].sum())))
            if ((c.year, c.month)) in data['time_table'].index:

                heatmap_data[hour].append(max(1,int(data['time_table'].loc[c.year, c.month].sum(level='time(24h)').loc[start_hour:end_hour].sum())))
            else:
                heatmap_data[hour].append(1)

    x_ticks_label = data['month_span_str']
    p2 = {
        'x_ticks_label':x_ticks_label,
        'y_ticks_label': hours,
        'heatmap_data': heatmap_data
    }

    return p2

def prep_3(data):

    #using data['time_table']
    
    #initialize
    weekday = 7
    heatmap_data = {key : [1]*weekday for key in ['%02d:00-%02d:00' % (h, h+1) for h in xrange(24)]}
    #data['month']

    heatmap_data['23:00-23:59'] = heatmap_data.pop('23:00-24:00')
    calender = sorted(set(zip(data['time_table'].index.to_series().str[0],data['time_table'].index.to_series().str[1])))
    hours = sorted(heatmap_data.keys())

    for hour in hours:
        start_hour, end_hour = hour.split('-')
        start_hour = datetime.strptime(start_hour, '%H:%M').time()
        end_hour = datetime.strptime(end_hour, '%H:%M').time()

        days = list(data['time_table'].sum(level=['time(24h)', 'weekday']).loc[start_hour:end_hour].sum(level='weekday').index)

        for day in days:

            heatmap_data[hour][day] = max(1,int(data['time_table'].sum(level=['time(24h)', 'weekday']).loc[start_hour:end_hour].sum(level='weekday').loc[day]))


    p3 = {
        'y_ticks_label': hours,
        'heatmap_data': heatmap_data
    }

    return p3

def prep_4(data):

    #using data['logs']
    
    #every 50 as a level
    span = 50
    #totally 5 levels
    levels = 5

    #vc = np.arange(0,306,51)
    vc = np.arange(0, span*levels+levels, span+1)
    #vc: array([  0,  31,  62,  93, 124, 155])
    legend_label = ['-'.join([str(x[0]), str(x[1])]) for x in zip(vc[:-1], vc[1:]-1)]
    legend_label = ['访问数在' + x + '之间的用户数占比：' for x in legend_label]
    #legend_label.append('访问数在255以上的用户占比：')
    legend_label.append('访问数在{}以上的用户占比：'.format(vc[-1]))

    total_users = len(data['logs']['userid'].unique())
    visits_group_by_users = data['logs'].groupby('userid')['visit'].sum().fillna('0')
    level_mask = [visits_group_by_users.apply(lambda x: x<i+span and x>i) for i in vc[:-1]]
    slices = [visits_group_by_users[x] for x in level_mask]
    slices = [len(x) for x in list(slices)]
    slices.append(len(visits_group_by_users[visits_group_by_users>vc[-1]]))
    percents = [100.0*x/total_users for x in slices]
    legend_label = [x[0]+"{:4.2f}".format(x[1]) for x in zip(legend_label, percents)]
    
    p4 = {
        'total_users':total_users,
        'legend_label':legend_label,
        'slices': slices
    }

    return p4

def prep_5(data):
    #placeholder
    p5 = {
        
    }

    return p5

def prep_6(data):

    #using data['day_span'], data['logs'], data['start_date'], data['left_offset'], data['months']
    
    #Plotting of every day's statistics of three kinds of users, see the detail of these definition in my thesis!
    #s1: Newly added hibernated users per day
    #s2: Active users per day
    #s3: New comers per day
    #u_all: Total users by then
    s1 = []
    s2 = []
    s3 = []
    u_all = set([])
    #visits = []
        
    #1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
    #0 1 2 3 4 5 6 0 1 2  3  4  5  6  0

    for i in xrange(data['day_span']):

        mask = (data['logs']['time'] > data['start_date']+timedelta(days=i-6)) & (data['logs']['time'] <= (data['start_date'] + timedelta(days=i)))
        u_s2 = set(data['logs'].loc[mask]['userid'].unique())
        u_s1 = u_all - u_s2
        u_s3 = u_s2 - u_all
                
        s1.append(len(u_s1))
        s2.append(len(u_s2))
        s3.append(len(u_s3))
        #update 
        u_all = u_all.union(u_s2)
                

    #since month_span_str is less a month than month_span_list it'd better not modify here and regenerate again:
    x_ticks_label = pd.date_range(start = data['months'][0], periods = data['month_span'], freq = 'MS').format(formatter=lambda x: x.strftime('%Y-%m'))
        
    p6 = {
        's1': s1,
        's2': s2,
        's3': s3,
        'u_all':u_all,
        'left_offset':data['left_offset'],
        'months':data['months'],
        'x_ticks_label':x_ticks_label,
        #'visits': visits
    }
    return p6   

def prep_7(data):
    
    ip_db_file = init.ip_db_file
    
    def get_record_str(ip_db, offset = 0):
            
        o2 = ip_db.find('\0', offset)
        gb2312_str = ip_db[offset:o2]
        try:
            utf8_str = unicode(gb2312_str,'gb2312').encode('utf-8')
        except:
            return '未知'
        return utf8_str
     
    def get_record_offset(ip_db, offset = 0):
        s = ip_db[offset: offset + 3]
        s += '\0'
        return unpack('<I', s)[0]
     
    def get_area_info(ip_db, offset = 0):
            
        byte = ord(ip_db[offset])
        if byte == 1 or byte == 2:
            p = get_record_offset(ip_db, offset + 1)
            return get_area_info(ip_db, p)
        else:
            return get_record_str(ip_db, offset)
     
    def get_info(ip_db, offset, ip = 0):
        o = offset
        byte = ord(ip_db[o])
     
        if byte == 1:
            return get_info(ip_db, get_record_offset(ip_db, o + 1))
            
        if byte == 2:
            cArea = get_area_info(ip_db, get_record_offset(ip_db, o + 1))
            o += 4
            aArea = get_area_info(ip_db, o)
            return (cArea, aArea)
                
        if byte != 1 and byte != 2:
            
            cArea = get_record_str(ip_db, o)
            o = ip_db.find('\0', offset) + 1
            aArea = get_record_str(ip_db, o)
            return (cArea, aArea)
     
    def find(ip_db, first_i, ip, l, r):
        if r - l <= 1:
            return l
     
        m = (l + r) / 2
        o = first_i + m * 7
        new_ip = unpack('<I', ip_db[o: o+4])[0]
     
        if ip <= new_ip:
            return find(ip_db, first_i, ip, l, m)
        else:
            return find(ip_db, first_i, ip, m, r)
            
    def query_ip_info(ip_db, index_c, first_i, ip):
        try:
            check_ip = socket.inet_aton(ip)
        except socket.error as e:
            logger.info('Error IP: ' + ip)
            return ('未知', '未知', '未知', '未知', '未知')
        
        ip = unpack('!I', check_ip)[0]
        i = find(ip_db, first_i, ip, 0, index_c - 1)
        o = first_i + i * 7
        o2 = get_record_offset(ip_db, o + 4)
        (area, isp) = get_info(ip_db, o2 + 4)


        #import ipdb; ipdb.set_trace()
        isp = unicode(isp, 'utf-8')
        isp = isp if isp != u'\x02G' else u'电信'
        province_regex = r"((?:辽宁|吉林|黑龙江|河北|山西|陕西|甘肃|青海|山东|安徽|江苏|浙江|河南|湖北|湖南|江西|台湾|福建|云南|海南|四川|贵州|广东)(?:省)?|(?:西藏)(?:自治区)?|(?:内蒙古)(?:自治区)?|(?:新疆)(?:(?:维吾尔)?自治区)?|(?:宁夏)(?:回族自治区)?|(?:广西)(?:壮族自治区)?)?"
        m1 = re.split(province_regex, area)

        
        if len(m1) == 0:

            country = unicode(area, 'utf-8')
            #print(country+'|||')
            return (country, '', '', '', isp)

        elif len(m1)>1:
            country = u'中国'

            province = unicode(m1[1], 'utf-8') if m1[1] is not None else ''

            if len(m1)>2:

                city_regex = ur"(上海|北京|重庆|天津|(?:[^市县区]+)市)?"
                m2 = re.split(city_regex, unicode(m1[2], 'utf-8'))
                
                if len(m2) == 0:
                    
                    city = ''
                    district = ''
                    return (country, province, city, district, isp)
            
                elif len(m2)==1:
                    
                    city = m2[0] if m2[0] is not None else ''
                    district = ''
                    return (country, province, city, district, isp)
                
                elif len(m2)>2:
                    
                    city = m2[1] if m2[1] is not None else ''
                    
                    if not m2[2]:
                        
                        district = ''
                        return (country, province, city, district, isp)
                    
                    else:
                        district_regex = ur"([^市县区]+(?:市|县|区))"
                        m3 = re.split(district_regex, m2[2])

                        if not m3:
                            district = ''
                            return (country, province, city, district, isp)
                        elif len(m3) >0:
                            district = m3[1] if m3[1] is not None else ''
                            return (country, province, city, district, isp)
                elif len(m2)==2:

                    logger.info("Encounter error when using regex to parse area string!")

        elif len(m1) == 1:
            country = u'中国'
            return (country, '', '', '', isp)
                
    def gen_freqs(ip_geo_dict, ip_cnt, ip_list, type):
        #type can be province, city, isp
        freqs = pd.DataFrame([(ip_geo_data[i][type], ip_cnt[i]) for i in ip_list], columns=[type, 'weight'])
        #freqs = tuple(freqs.groupby('city')['weight'].sum())
        freqs.set_index(type, inplace=True)
        freqs = freqs.groupby(freqs.index).sum().to_dict()['weight']
        #key_to_delete = max(freqs, key=lambda k: freqs[k])

        if '' in freqs:
            del freqs['']
        if '未知' in freqs:
            del freqs['未知']
        return freqs

    ##---------------------
    ip_geo_data = {}
    
    with open(ip_db_file, 'rb') as f:
        ip_database = f.read()
     
    (first_index, last_index) = unpack('<II', ip_database[:8])
    index_count = (last_index - first_index) / 7 + 1
     
    ip_cnt = dict(data['logs'].groupby('ip')['visit'].sum())
    ip_list = ip_cnt.keys()
    for ip in ip_list:
        (n, p, c, d, i) = query_ip_info(ip_database, index_count, first_index, ip)
        ip_geo_data[ip] = {
            'country': n,
            'province': p,
            'city':c,
            'district': d,
            'isp': i
        }
        print(ip, '|', n, '|', p, '|', c, '|', d, '|', i)
       
    freqs_p = gen_freqs(ip_geo_data, ip_cnt, ip_list, 'province')
    freqs_c = gen_freqs(ip_geo_data, ip_cnt, ip_list, 'city')
    freqs_i = gen_freqs(ip_geo_data, ip_cnt, ip_list, 'isp')
    #freqs = [(k,v) for k,v in freqs.iteritems()]

    p7 = {
        'ip_geo_data':ip_geo_data,
        'freqs':{
            'province': freqs_p,
            'city': freqs_c,
            'isp': freqs_i
        }
    }

    return p7

def prep_8(data):

    #using data['logs']

    #-------------    
    #metric 1: 课程用户活跃度=访问次数在threshold_1以上用户数/历史在线用户数

    threshold = 60

    total_users = len(data['logs']['username'].unique())
    
    visits_group_by_users = data['logs'].groupby('username')['visit'].sum().fillna('0')
    visit_level = visits_group_by_users.apply(lambda x: x>threshold)
    
    users_beyond_threshold = len(visits_group_by_users[visit_level])
    metric_1 = 1.0*users_beyond_threshold/total_users

    #-------------    
    #metric 2：人均课程使用时间=历史用户总在线时长/课程历史访问用户数

    online_time = data['logs'].groupby('session_id')['session_interval'].sum().dropna().sum().seconds
    metric_2 = 1.0*online_time/total_users

    #-------------    
    #metric3: 人均论坛访问量=论坛总访问量/历史在线用户数 — 表征论坛的总体使用情况
    #论坛总访问量 = 统计所有“forum”打头的actionname:
    forum_total_visits = data['logs'][data['logs']['eventname'].str.contains('\\mod_forum')]['visit'].sum()
    metric_3 = 1.0*forum_total_visits/total_users

    #-------------
    #metric_4: #论坛发帖、回帖总数=统计所有“forum add"打头的actionname
    condition_m4 = ['\\mod_forum\\event\\discussion_created', '\\mod_forum\\event\\post_created']

    metric_4 = data['logs'][data['logs']['eventname'].isin(condition_m4)]['visit'].sum()

    #-------------    
    #metric_5: 论坛发帖回复率=论坛回帖数/论坛主题数
    #论坛回帖数:
    forum_add_post = data['logs'][data['logs']['eventname']==condition_m4[1]]['visit'].sum()
    #论坛主题数:
    forum_add_discussion = data['logs'][data['logs']['eventname']==condition_m4[0]]['visit'].sum()     
    metric_5 = (1.0*forum_add_post/forum_add_discussion) if forum_add_discussion else 0

    #-------------    
    #metric6: 论坛生命力=贡献内容（发帖回帖）的用户数/曾访问论坛的全部用户数
    #贡献内容（发帖回帖）的用户数:
    forum_add_content_users = len(data['logs'][data['logs']['eventname'].isin(condition_m4)]['username'].unique())
    forum_total_users = len(data['logs'][data['logs']['eventname'].str.contains('\\mod_forum')]['username'].unique()) 

    metric_6 = (1.0*forum_add_content_users/forum_total_users) if forum_total_users  else 0


    p8 = {
        'metrics':[metric_1, metric_2, metric_3, metric_4, metric_5, metric_6]       }

    return p8
    

def prep_9(data):

    #using data['logs'], data['left_offset'], data['month_span_str']
    
    df9 = data['logs'][['username', 'session_interval', 'eventname']]
    df9['day'] = data['logs']['time'].apply(lambda x: datetime.date(x))

    #each day bool mask
    days = [(data['logs']['time'] > i) & (data['logs']['time'] <= (i + timedelta(days=1))) for i in list(data['day_index'])]

    #events happened each day
    each_day_events = [df9.loc[each_day][['eventname', 'session_interval']].fillna(0) for each_day in days]

    #total visiting users each day
    each_day_users = [len(data['logs'].loc[each_day]['username'].unique()) for each_day in days]

    def action_time_of_day(each_day, regexp, contains):

        if contains:
            #each day's events which match the regex
            each_day_events = [each_day[i][each_day[i]['eventname'].str.contains(regexp)] for i in xrange(len(each_day))]

        else:
            #each day's events which unmatch the regex, which means the others comparing to above
            each_day_events = [each_day[i][~each_day[i]['eventname'].str.contains(regexp)] for i in xrange(len(each_day))]

        #each day's events' total online time, after filtering by regex above
        return [x['session_interval'].sum().seconds/60.0 for x in each_day_events]
        
    #-------
    #total online time and its avg for events associated with course, each within a day
    course = action_time_of_day(each_day_events, '^\\\\core\\\\event\\\\course_', True)
    course_avg = [1.0*course[i]/each_day_users[i] if each_day_users[i] else 0 for i in xrange(len(course))]
    
    #-------
    #total online time and its avg for events associated with forum, each within a day

    forum = action_time_of_day(each_day_events, '^\\\\mod_forum', True)
    forum_avg = [1.0*forum[i]/each_day_users[i] if each_day_users[i] else 0 for i in xrange(len(forum))]
    
    #-------
    #total online time and its avg for events associated with page, each within a day
    page = action_time_of_day(each_day_events, '^\\\\mod_page', True)
    page_avg = [1.0*page[i]/each_day_users[i] if each_day_users[i] else 0 for i in xrange(len(page))]
    
    #-------
    #total online time and its avg for events associated with quiz, each within a day
    quiz = action_time_of_day(each_day_events, '^\\\\mod_quiz', True)
    quiz_avg = [1.0*quiz[i]/each_day_users[i] if each_day_users[i] else 0 for i in xrange(len(quiz))] 

    #-------
    #total online time and its avg for events associated except above modules, each within a day
    others = action_time_of_day(each_day_events, '^\\\\core\\\\event\\\\course_|^\\\\mod_forum|^\\\\mod_page|^\\\\mod_quiz', False)
    others_avg = [1.0*others[i]/each_day_users[i] if each_day_users[i] else 0 for i in xrange(len(others))] 

    #-------
    #total online time and its avg for events, each within a day
    total = [x['session_interval'].sum().seconds/60.0 for x in each_day_events]
    total_avg = [1.0*total[i]/each_day_users[i] if each_day_users[i] else 0 for i in xrange(len(total))]

    #x_ticks_label = pd.date_range(start = data['months'][0], periods = data['month_span'], freq = 'MS').format(formatter=lambda x: x.strftime('%Y-%m'))
    
    p9 = {
        'total': total_avg,
        'forum': forum_avg,
        'course': course_avg,
        'page': page_avg,
        'quiz': quiz_avg,
        'others': others_avg,
        'left_offset': data['left_offset'],
        #'right_offset': data['right_offset'],
        #'months': data['months'],
        'x_ticks_label': data['month_span_str'],
        
    }

    return p9

def prep_10(data):

    #using data['logs'], data['day_index'], data['left_offset'], data['start_date'], data['end_date']
    
    df1 = data['logs'][['session_interval']]
    
    #switch off pandas' SettingWithCopyWarning !
    pd.reset_option('mode.chained_assignment')
    with pd.option_context('mode.chained_assignment', None):
        df1['date'] = data['logs']['time'].apply(lambda x: datetime.date(x))
    df1 = df1.groupby('date')['session_interval'].sum().to_frame().fillna(0)
    df2 = pd.DataFrame(index = data['day_index'], columns=['session_interval']).fillna(0)
    df1 = (df1+df2).fillna(0)

    days = [(data['logs']['time'] > i) & (data['logs']['time'] <= (i + timedelta(days=1))) for i in list(df1.index)]
    users_cnts = [len(data['logs'].loc[each_day]['username'].unique()) for each_day in days]

    df1['users'] = users_cnts
    #by minutes
    df1['avg_online_time'] = \
                             [1.0*df1['session_interval'].iloc[i].seconds/(df1['users'].iloc[i]*60) \
                              if df1['users'].iloc[i] else 0 \
                              for i in xrange(len(df1.index))]

    p10 = {
        'left_offset': data['left_offset'],
        #'right_offset': data['right_offset'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'online_stats': df1,
        #'months': data['months'],
        #'x_ticks_label': data['month_span_str'],
    }

    return p10
