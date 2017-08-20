def amend(baseurl, url_func_list):

    url_func_list['\\core\\event\\course_viewed'] = {#mal struct of get_url in func scan
        'param': ['courseid',],
        'url_template': baseurl + "course/view.php?id={}"
    }
    url_func_list['\\mod_page\\event\\course_module_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/page/view.php?id={}"
    }
    url_func_list['\\mod_quiz\\event\\course_module_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/quiz/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\submission_status_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\submission_form_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\assignsubmission_onlinetext\\event\\assessable_uploaded'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\assignsubmission_onlinetext\\event\\submission_created'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\assignsubmission_file\\event\\assessable_uploaded'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\assignsubmission_file\\event\\submission_created'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\submission_confirmation_form_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\statement_accepted'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\assessable_submitted'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_glossary\\event\\course_module_viewed'] = {#mal struct of get_url in func scan
        'param': ['objecttable', 'contextinstanceid', "other['mode']"],
        'url_template': baseurl + "mod/{}/view.php?id={}&mode={}"
    }
    url_func_list['\\mod_feedback\\event\\course_module_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/feedback/view.php?id={}"
    }
    url_func_list['\\mod_resource\\event\\course_module_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/resource/view.php?id={}"
    }
    url_func_list['\\assignsubmission_onlinetext\\event\\submission_updated'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\assignsubmission_file\\event\\submission_updated'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\gradereport_user\\event\\grade_report_viewed'] = {#get_url not found in func scan
        'param': ['courseid',],
        'url_template': baseurl + "grade/report/user/index.php?id={}"
    }
    url_func_list['\\gradereport_overview\\event\\grade_report_viewed'] = {#get_url not found in func scan
        'param': ['courseid',],
        'url_template': baseurl + "grade/report/overview/index.php?id={}"
    }
    url_func_list['\\assignsubmission_comments\\event\\comment_created'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\core\\event\\course_user_report_viewed'] = {#func scan ignore it
        'param': ['courseid', 'relateduserid', "other['mode']"],
        'url_template': baseurl + "course/user.php?id={}&user=119&mode={}"
    }
    url_func_list['\\mod_url\\event\\course_module_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/url/view.php?id={}"
    }
    url_func_list['\\mod_forum\\event\\course_searched'] = {#get_url not found in func scan
        'param': ['courseid', "other['searchterm']"],
        'url_template': baseurl + "mod/forum/search.php?id={}&{}"
    } #default searchterm is 'search'
     
    url_func_list['\\mod_assign\\event\\grading_table_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\submission_graded'] = {#get_url not found in func scan
        #'param': ['courseid', "other['itemid']", 'relateduserid'],
        'param': ['courseid', "objectid", 'relateduserid'],
        'url_template': baseurl + "grade/edit/tree/grade.php?courseid={}&itemid={}&userid={}"
    }
    url_func_list['\\mod_assign\\event\\grading_form_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_assign\\event\\submission_viewed'] = {#get_url not found in func scan
        'param': ['contextinstanceid',],
        'url_template': baseurl + "mod/assign/view.php?id={}"
    }
    url_func_list['\\mod_forum\\event\\user_report_viewed'] = {#get_url not found in func scan
        'param': ['userid', "other['reportmode']", 'courseid'],
        'url_template': baseurl + "mod/forum/user.php?id={}&mode={}&course={}"
    }
    url_func_list['\\mod_forum\\event\\course_module_instance_list_viewed'] = {#get_url not found in func scan
        'param': ['courseid',],
        'url_template': baseurl + "mod/forum/index.php?id={}"
    }
    url_func_list['\\mod_glossary\\event\\entry_viewed'] = {#get_url not found in func scan
        'param': ['objectid',],
        'url_template': baseurl + "mod/glossary/showentry.php?eid={}"
    }
    url_func_list['\\mod_forum\\event\\post_created'] = {#get_url not found in func scan
        'param': ["other['discussionid']", 'objectid',],
        'url_template': baseurl + "mod/forum/discuss.php?d={}#p{}"
    }
    url_func_list['\\mod_quiz\\event\\course_module_instance_list_viewed'] = {#get_url not found in func scan
        'param': ['courseid',],
        'url_template': baseurl + "mod/quiz/index.php?id={}"
    }
    url_func_list['\\mod_forum\\event\\post_updated'] = {#get_url not found in func scan
        'param': ["other['discussionid']", 'objectid',],
        'url_template': baseurl + "mod/forum/discuss.php?d={}#p{}"
    }
    url_func_list['\\gradereport_grader\\event\\grade_report_viewed'] = {#get_url not found in func scan
        'param': ['courseid'],
        'url_template': baseurl + "grade/report/grader/index.php?id={}"
    }                       

    return url_func_list
