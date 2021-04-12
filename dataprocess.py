#things to remember:
# you took credit as float
#lab class ekta kore dhorsi always
#shob section ke alada course hishabe chinta korsi
import pandas as pd 
import numpy as np
import math
import datetime
courselist = []
teacherlist = []
sectionthree = []
dict_credit = {}
teacher_course_mp = {}
class Routine:
    def __init__(self, teacher_initial, time, course):
        self.teacher_initial = teacher_initial
        self.time = time
        self.course = course

class Course:
    def __init__(self, course_name, credit, course_year, lab_course, class_cnt):
        self.course_name = course_name
        self.credit = credit
        self.course_year = course_year    
        self.lab_course = lab_course 
        self.class_cnt = class_cnt
        if(self.lab_course == True):
            self.duration = datetime.timedelta(hours=3)
        elif(self.credit == 3):
            self.duration = datetime.timedelta(hours=1.5)
        elif(self.credit == 2):
            self.duration = datetime.timedelta(hours=1)

        
class Teacher:
    def __init__(self, teacher_initial, assigned_courses, valid_time):
        self.teacher_initial = teacher_initial
        self.assigned_courses = assigned_courses
        self.valid_time = valid_time   


def process_curriculum():
    df_curr = pd.read_excel("input.xlsx", "Sheet4")
    curr_matrix = df_curr.to_numpy()
    i = 0
    for i in range((curr_matrix.shape[0])):
        dict_credit[curr_matrix[i][1]] = float(curr_matrix[i][2])

def process_classcnt(credit, is_lab):
    if(is_lab == True):
        return 1
    if(credits == 3.0):
        return 2
    if(credits == 2):
        return 2
    else:
        return 2

def check_unique_course(crs_name):
    for i in range(len(courselist)):
        if(courselist[i].course_name == crs_name):
            return False
    return True

def process_course():
    #reading data from undergradcurriculum for courses
    df_course = pd.read_excel("input.xlsx", "Sheet2")
    course_matrix = df_course.to_numpy()
    for i in range(course_matrix.shape[0]):
        for j in range(course_matrix.shape[1]):
            if(pd.isnull(course_matrix[i][j]) or j == 0):
                continue
            chunks = course_matrix[i][j].split(' ')
            crs_chk = chunks[0] + ' ' + chunks[1]
            if(crs_chk in dict_credit):
                crs_credit = dict_credit[crs_chk]
            else: 
                continue
            crs_year = int(chunks[1][0])
            crs_lab = (chunks[1][2] == '1')
            crs_classcnt = process_classcnt(crs_credit, crs_lab)
            
            if(check_unique_course(course_matrix[i][j]) == True):
                teacher_course_mp[course_matrix[i][j]] = []
                C = Course(course_matrix[i][j], crs_credit, crs_year, crs_lab, crs_classcnt)
                courselist.append(C)
            teacher_course_mp[course_matrix[i][j]].append(course_matrix[i][0])
    # i = 0
    # for i in range(len(courselist)):
    #     print(courselist[i].course_name + ' ' + str(courselist[i].credit) + ' ' + str(courselist[i].course_year) + ' ' + str(courselist[i].lab_course) + ' ' + str(courselist[i].class_cnt))

def process_teacher():
    #reading data from assigned and validtimeslots for teachers
    df_assignedcourses = pd.read_excel("input.xlsx", "Sheet2")
    df_validtimeslot = pd.read_excel("input.xlsx", "Sheet3")
    assignedcrs_matrix = df_assignedcourses.to_numpy()
    validtime_matrix = df_validtimeslot.to_numpy()
    i = 0
    j = 0
    for i in range(assignedcrs_matrix.shape[0]):
        crslist = []
        for j in range(assignedcrs_matrix.shape[1]):
            if(j == 0):
                continue
            if(pd.isnull(assignedcrs_matrix[i][j]) == False):
                crslist.append(assignedcrs_matrix[i][j])
                section_str = assignedcrs_matrix[i][j].split(' ')
                if(len(section_str) == 4 and int(section_str[3][0]) == 3):
                    sectionthree.append(section_str[0] + ' ' + section_str[1])

        t_name = assignedcrs_matrix[i][0]
        t_idx = int(0)
        for k  in range(validtime_matrix.shape[0]):
            if(validtime_matrix[k][0] == t_name):
                t_idx = k
                break    

        temp_list = []
        for j in range(validtime_matrix.shape[1]):
            if(j == 0 or j==1 or j==7):
                continue
            if(pd.isnull(validtime_matrix[t_idx][j]) == False):
                temp_list.append(time_convert(validtime_matrix[t_idx][j]))
            else:
                temp_list.append([])
        teacherlist.append(Teacher(assignedcrs_matrix[i][0], crslist, temp_list))        
                
    
def time_convert(str):
    time_array = str.split(';')
    timelist = []
    for t in time_array:
        startTime = t.split('-')[0]
        startTime = datetime.datetime.strptime(startTime, '%I:%M%p')
        endTime = t.split('-')[1]
        endTime = datetime.datetime.strptime(endTime, '%I:%M%p')
        timelist.append([startTime, endTime])
    return timelist


process_curriculum()
process_course()
process_teacher()
# t_name = assignedcrs_matrix[i][0]
        # t_idx = int(0)
        # for k  in range(validtime_matrix.shape[0]):
        #     if(validtime_matrix[k][0] == t_name):
        #         t_idx = k
        #         break