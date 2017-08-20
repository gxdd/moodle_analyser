# # -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os

import pandas as pd
from datetime import datetime, timedelta
import cPickle

import MySQLdb as mdb
from six import string_types
import subprocess
import types
import gzip
import glob
import re
import amended_urls
from plots_register import *

import logging
import logging.config


logging.config.fileConfig('./logging.conf')
#logger = logging.getLogger('__name__')
logger = logging.getLogger("example01")

if not os.path.exists('data/'):
    os.makedirs('data/')

event_files_list_pickle_file = 'event_files_list.cpklz'
urls_pickle_file = 'urls.cpklz'

#do not forget the ending slash!!
baseurl = 'http://localhost:9999/moodle31/'    
docroot = '/Applications/MAMP/htdocs/moodle31/'

ip_db_file = './misc/qqwry.dat'

font_lib = {
    '华文仿宋':'./misc/hwfs.ttf',
    '微软雅黑':'./misc/msyh.ttf',
    }

dsn_config = {
    'host': '127.0.0.1',
    'port': 8889,
    'user': 'moodle',
    'passwd': 'moodle',
    'db': 'moodle31',
#    'charset': 'utf8'
}

##--------------------------------------

# without changing unix_timestamp
def gen_log_query(courseid):
    mdl_logstore_standard_log_query= '''SELECT 
from_unixtime(b.timecreated) as 'time'
, b.timecreated
, a.username
, b.userid
, CONCAT(a.firstname, a.lastname) as 'studentname'
, b.courseid
, c.fullname as coursename
, b.action
, b.eventname
, b.component
, b.contextid
, b.contextlevel
, b.contextinstanceid
, b.objecttable
, b.objectid
, b.relateduserid
, b.other
, b.ip 
FROM mdl_user a
, mdl_logstore_standard_log b
, mdl_course c 
WHERE c.idnumber = '{}'
AND b.userid = a.id 
AND b.courseid = c.id
ORDER BY b.userid, b.timecreated ASC'''.format(courseid)

    return mdl_logstore_standard_log_query

def query_db_log(dsn_config, courseid):

    try:
        
        conn = mdb.connect(**dsn_config)
        log_query = gen_log_query(courseid)
        
        with conn:
            cur = conn.cursor(mdb.cursors.Cursor)
            cur.execute(log_query)
            logger.info('courseid {}: Dumping logs initially from database...'.format(courseid))
            col_names = [i[0] for i in cur.description]
            logs = cur.fetchall()
            logger.info('Done log dumping!')
            cur.close()
        conn.close()
 
    except mdb.DataError as e:
        print("DataError")
        print(e)
 
    except mdb.InternalError as e:
        print("InternalError")
        print(e)
 
    except mdb.IntegrityError as e:
        print("IntegrityError")
        print(e)
 
    except mdb.OperationalError as e:
        print("OperationalError")
        print(e)
 
    except mdb.NotSupportedError as e:
        print("NotSupportedError")
        print(e)
 
    except mdb.ProgrammingError as e:
        print("ProgrammingError")
        print(e)
 
    except :
        print("Unknown error occurred")
        
    return (logs, col_names)


def load_data(cpickle_file):
    
    logger.info('Loading cpickle file : {}...'.format(cpickle_file))
    
    p = pd.read_pickle(cpickle_file, compression="gzip")
    
    logger.info('Done data loading!')

    return p

def dump_data(cpickle_file, data):
    
    with gzip.open(cpickle_file,"wb") as f:
        logger.info('Dumping cpickle file : {}...'.format(cpickle_file))
        cPickle.dump(data, f, protocol=2)
        logger.info('Done data dumping!')
        
def prepare_event_files(event_files_list_pickle_file, htdocs_root):

    if not os.path.exists(event_files_list_pickle_file):

        logger.info('Event files list not ready, generate it first:')
        logger.info('Scanning for PHP files which has get_url() defined...')

        extractor_one_liner = "find \"$(cd %s..; pwd)\" -iname '*.php' -type f -exec pcregrep -l --buffer-size=200K -HM 'public function get_url()' '{}' \\;|grep classes\\/event|awk '{print $1}' FS=':'" % (htdocs_root)
        
        files = subprocess.check_output(extractor_one_liner, shell=True)

        logger.info('Done scanning!')
        
        files = files.split('\n')
        files = [i for i in files if i is not '']

        logger.info('Storing event files list for future extraction...')

        dump_data(event_files_list_pickle_file, files)

        logger.info('Done storing event files list!')
    
        return files

    else:

        logger.info('Event files list exist, loading...')
        
        data = load_data(event_files_list_pickle_file)

        logger.info('Done loading event files list!')
        return data
        


def get_event_url_templates(file_list=None):

# function to iterate moodle events class files and analysis get_url method to acquire the url pattern

    if file_list is not None: #need to generate urls template file from scratch

        logger.info('Event url templates is not ready, preparing it first...')

        url_func_list = {}
        component_book = {'lib/classes':'core'}
    
        for l in file_list:
            
            path_matches = re.search(r"%s(.+)/classes/event/(.+)\.php" % docroot, l)
            if path_matches is not None:
                
                (component, event) = path_matches.groups()
                component = "_".join(re.search('(.+)', component).group(1).split('/'))
         
                if component == 'lib':
                    component = 'core'
                eventname = "\\"+ "\\".join((component, "event", event))
         
                #start search for function definition:
                file_content = open(l.lstrip().rstrip(), 'r').read()
                    
                func_matches = re.search(r"public function\s*get_url[(].*[)]\s*{\n[\w\W]+return new \\*moodle_url[(]'?/([\w\/.$]+)'?(, array[(]\n*([\w\W]+)\n*[)])?[)];", file_content, re.M)
         
                if func_matches:
     
                    path = func_matches.groups()[0]
                    var_section = func_matches.groups()[2]
                
                    if var_section is not None:
                        
                        param_attrs = ""
                        param_values = []
                        param_list = re.findall(r"'(\w+)'\s*=>\s*(\$this->)?('?\w+'?(\['\w+'\])?)", var_section, re.M)
                                                 
                        if param_list is not None:
                            for p in param_list:
                                if re.match(r"'\w+'", p[2]):
                                    param_attrs += p[0] + "=" + p[2] +"&"
                                else:
                                    param_attrs += p[0]+"={}&"
                                    param_values.append(p[2])
                        else:
                            pass
                            #print("param extract failed:",var_section,"in:",l)
         
                        url_func_list[eventname] = {
                            'param': tuple(param_values),
                            'url_template': baseurl + path + "?" + param_attrs[0:-1]
                        }
         
                    else:
                        #print("mismatch pattern when extracting var_section.")
                        url_func_list[eventname] = {
                            'param': None,
                            'url_template': baseurl + path
                        }
                    
                else:
                    pass
                    #print("mal structure of function get_url():",l.rstrip().lstrip(),"|",eventname)
            
            else:
                pass
                #print("skipping:",l)
                #print("mismatch pattern for path:",l)
     
        #all these come from analysis of relative web log url pattern, manually added
        logger.info('Amending url templates by appending manually url templates...')
        amended_urls.amend(baseurl, url_func_list)
     
        logger.info('Done amending, dumping for permanent access...')
        
        dump_data(urls_pickle_file, url_func_list)

        logger.info('Done dumping')
        
        
    else:

        logger.info('Url templates file exists, loading...')
        
        url_func_list = load_data(urls_pickle_file)
        #amended_urls.amend(baseurl, url_func_list)
        #dump_data(urls_pickle_file, url_func_list)

        logger.info('Done loading url templates file!')
        

    logger.info('Url template file is ready!')
    return url_func_list 



def prep_basic_stats(courseid):


    if not os.path.exists(urls_pickle_file):

        file_list = prepare_event_files(event_files_list_pickle_file, docroot)
        event_url_templates = get_event_url_templates(file_list)
        
    else:
        event_url_templates = get_event_url_templates(None)

    logs, col_names = query_db_log(dsn_config, courseid)

    logger.info('courseid {}: Start munging log data ...'.format(courseid))

    #columns contains NaN will store non-NaN as float, convert to int before using those cells
    df = pd.DataFrame(list(logs))
    df.columns = col_names
    
    df = df.sort_values(by =['userid', 'time'], ascending=[True, True])
    #actual time series in different level
    year_list = [d.year for d in df['time']]
    month_list = [d.month for d in df['time']]
    day_list = [d.day for d in df['time']]
    time_list = [d.time() for d in df['time']]
    time_table = pd.DataFrame(list(zip(year_list, month_list, day_list, time_list)), columns=['year', 'month', 'day', 'time(24h)'])
    time_table["weekday"] = [(x.weekday()+1)%7 for x in df["time"]]
    time_table['visit'] = 1
    time_table.set_index(["year", "month", "day", "time(24h)", "weekday"], inplace=True)
    time_table.index.set_levels(time_table.index.levels[0].astype(int), level=0, inplace=True)
    time_table.index.set_levels(time_table.index.levels[1].astype(int), level=1, inplace=True)
    time_table.index.set_levels(time_table.index.levels[2].astype(int), level=2, inplace=True)
    time_table.sort_index(axis=0, ascending=True, inplace=True)

    gt_30min = df['time'].diff() > timedelta(minutes=30) 
    diff_user = df['userid'].diff() > 0
    session_id = (diff_user | gt_30min).cumsum() 
    df['session_id'] = session_id
    df['session_interval'] = df.groupby('session_id')['time'].diff()
    df['session_interval'] = df['session_interval'].fillna(0)

    #define your ignored event list!!
    #by using any condition here!
    #for example if you want to filter out role assign event or if you want to filter out by user or by event type. 
    #df['visit'] = 1
    ignored_events = ['\\core\\event\\enrol_instance_created', '\\core\\event\\enrol_instance_deleted', '\\core\\event\\user_enrolment_created', '\\core\\event\\user_enrolment_deleted', '\\core\\event\\role_assigned']
    
    df['visit'] = np.where(df['eventname'].isin(ignored_events), 0, 1)
    
    start_date = df['time'].min().date()
    #start_day
    end_date = df['time'].max().date()
    end_date += timedelta(days=1)
    day_index = pd.date_range(start_date, end_date, freq='D')
    day_span = len(day_index)
     
    months = sorted(list(df['time'].apply(lambda x: x.strftime('%Y-%m')).unique()))

    start = datetime(df['time'].min().year, df['time'].min().month, 1)
    end = datetime(df['time'].max().year, df['time'].max().month+1, 1)
    month_span_list = pd.date_range(start, end, freq='MS')

    month_span = len(month_span_list)

    month_span_str = pd.date_range(*(pd.to_datetime([start_date, end_date]) + pd.offsets.MonthEnd()), freq='M').strftime('%Y-%m')
    month_span_str = list(month_span_str)
    
    left_offset = (df['time'].min() - month_span_list[0]).days
    right_offset = (month_span_list[-1]-df['time'].max()).days
    
    df['url'] = np.where(df['eventname'].isin(event_url_templates.keys()), "defined", "not_defined")
    
    url_not_defined_events = set()
    
    for index, row in df.iterrows():
            #print index
        if row['url'] == "defined":
            params =  event_url_templates[row['eventname']]['param']
            param_list = []
            for i in params:
                m1 = re.search(r"other\['(\w+)'\]", i)
                if m1 is not None:
                    key = m1.group(1)
                    if not isinstance(row['other'], string_types):

                        logger.info('Not proper type of other column!')
                        return None
                        
                    m2 = re.findall(r'((\w:)([0-9]+:)*"?([^{}:;"]+)"?;)((\w:)([0-9]+:)*"?([^{}:;"]*)"?;)', row['other'])
                    if m2:
                        other_dict = {}
                        for i in m2:
                            other_dict[i[3]]=i[7]
                    else:

                        logger.info('Regex error!')
                        return None

                    if key not in other_dict:

                        logger.info('Key error in logs\' other column!')
                    param_list.append(other_dict[key])
     
                else: #params do not include other column's attribute
                    
                    tmp = row[i]
                    if isinstance(tmp, float):
                        tmp = int(tmp)
                    param_list.append(tmp)
     
            df.set_value(index,'url', event_url_templates[row['eventname']]['url_template'].format(*param_list))

    else:
                           
        url_not_defined_events.add(row['eventname'])

    if len(url_not_defined_events):
                           
        logger.info('Below events\' url templates not defined:')
                           
        for i, x in enumerate(url_not_defined_events):
            print(i, x)
                           
        logger.info('Please manually add url patterns for these event and rerun this script!')
        
    data = {
        'courseid':courseid,
        'logs': df,
        #------------------logs is a Dataframe, with
        #columns: username	userid	studentname	courseid	coursename	action	eventname	component	contextid	contextlevel	contextinstanceid	objecttable	objectid	relateduserid	other	time	ip	session_id	session_interval	url
        #exp:
        #0	1345001251653	0	徐帅卿同学	4	国家开放大学学习指南DEL161	created	\core\event\user_enrolment_created	core	1211	50	4	user_enrolments	-31337.0	5163.0	a:1:{s:5:"enrol";s:6:"manual";}	2016-12-25 16:30:53	180.136.151.242	0	0 days	yes
        #first column is the auto index of pandas' Dataframe object
        #-------------------
        'time_table':time_table,
        'start_date': start_date,
        'end_date': end_date,
        'day_index': day_index,
        'months': months,
        'month_span_list':month_span_list,
        'month_span_str':month_span_str,
        'month_span':month_span,
        'day_span': day_span,
        'left_offset': left_offset,
        'right_offset': right_offset
    }
    #df.to_csv("dump.csv", sep='|', encoding='utf-8')
    course_pickle_file = './data/{}-{}.cpklz'.format(courseid, datetime.now().strftime("%Y%m%d-%H%M%S"))
    logger.info('Finished data munging, storing...')
    dump_data(course_pickle_file, data)
    logger.info('Data is mungged and ready!')
    return (data, course_pickle_file)


def prep_extended_stats(courseid, data, data_file_path, prep):

    methods = {
        '1': prep_1,
        '2': prep_2,
        '3': prep_3,
        '4': prep_4,
        '5': prep_5,  #ignore temporary, left as placeholder!
        '6': prep_6,
        '7': prep_7, 
        '8': prep_8,
        '9': prep_9, 
        '10': prep_10
    }

    if prep not in methods:
        logger.info('courseid {}: prep_{} plotting method not registered!'.format(courseid, prep))
        return None

    prep_pickles = re.search(r"(.*)\.cpklz", data_file_path).group(1)+"_{}.cpklz".format(prep)
                           
    logger.info('courseid {}: Preparing cpickle file for plot {}...'.format(courseid, prep))
    p_data = methods[prep](data)
    dump_data(prep_pickles, p_data)
    logger.info('courseid {}: Done generating p{} cpickle file!'.format(courseid, prep))

    return p_data

def init_data(courseid, prep):

    pat = re.compile(re.escape(courseid) + r"[^_]+\.cpklz")
    found = filter(pat.match, os.listdir("./data/"))
    if found != []:
        course_cpickle_file_path = max(["./data/"+f for f in found], key=os.path.getctime)

        logger.info('cPickle file for courseid {} found!'.format(courseid))
        prep_pickles = re.search(r"(.*)\.cpklz", course_cpickle_file_path).group(1)+"_{}.cpklz".format(prep)
        if not os.path.exists(prep_pickles):
            logger.info('courseid {}: prep_{} cpickle file not exists!'.format(courseid, prep))
            data1 = load_data(course_cpickle_file_path)
            data2 = prep_extended_stats(courseid, data1, course_cpickle_file_path, prep)

        else:
            
            data2 = load_data(prep_pickles)
    else:
        data1,path = prep_basic_stats(courseid)
        data2 = prep_extended_stats(courseid, data1, path, prep)

    return data2


