import pandas as pd 
import numpy as np
import math
import datetime
courselist = []
teacherlist = []
sectionthree = []
class Course:
    def __init__(self, course_name, credit, section_count, course_year, lab_course, class_cnt):
        self.course_name = course_name
        self.credit = credit
        self.section_count = section_count
        self.course_year = course_year    
        self.lab_course = lab_course 
        self.class_cnt = class_cnt

        
class Teacher:
    def __init__(self, teacher_initial, assigned_courses, valid_time):
        self.teacher_initial = teacher_initial
        self.assigned_courses = assigned_courses
        self.valid_time = valid_time


##functions
def process_class_cnt(credit):
    if(credit == 3):
        return 2
    elif(credit == 2):
        return 2
    elif(credit == 1.5):
        return 1
    elif(credit == .75):
        return 1

def process_course():

    #reading data from undergradcurriculum for courses
    df_course = pd.read_excel("ASST 03_ Input.xlsx", "UndergradCurriculum (Pre-fed)")
    course_matrix = df_course.to_numpy()
    i = 0
    for i in range(course_matrix.shape[0]):
        chunks = course_matrix[i][1].split(' ')
        if(chunks[1][2] == '1'):
            courselist.append(Course(course_matrix[i][1], course_matrix[i][2], 2, chunks[1][0], chunks[1][2] == '1', process_class_cnt(float(course_matrix[i][2]))))
        else:
            courselist.append(Course(course_matrix[i][1], course_matrix[i][2], 0, chunks[1][0], chunks[1][2] == '1', process_class_cnt(float(course_matrix[i][2]))))


def process_teacher():
    #reading data from assigned and validtimeslots for teachers
    df_assignedcourses = pd.read_excel("ASST 03_ Input.xlsx", "AssignedCourses")
    df_validtimeslot = pd.read_excel("ASST 03_ Input.xlsx", "ValidTimeSlots")
    assignedcrs_matrix = df_assignedcourses.to_numpy()
    validtime_matrix = df_validtimeslot.to_numpy()
    i = 0
    j = 0
    for i in range(assignedcrs_matrix.shape[0]):
        crslist = []
        timeslt = []
        for j in range(assignedcrs_matrix.shape[1]):
            if(j == 0):
                continue
            if(pd.isnull(assignedcrs_matrix[i][j]) == False):
                crslist.append(assignedcrs_matrix[i][j])
                section_str = assignedcrs_matrix[i][j].split(' ')
                if(len(section_str) == 4 and int(section_str[3][0]) == 3):
                    sectionthree.append(section_str[0] + ' ' + section_str[1])
                    

        for j in range(validtime_matrix.shape[1]):
            temp_list = []
            if(j == 0):
                continue
            if(pd.isnull(validtime_matrix[i][j]) == False):
                temp_list.append(time_convert(validtime_matrix[i][j]))
            else:
                temp_list.append('Not available')
            timeslt.append(temp_list)

        teacherlist.append(Teacher(assignedcrs_matrix[i][0], crslist, timeslt))        
                
    
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


def process_section():
    i = 0
    for i in range(len(sectionthree)):
        idx = [x.course_name for x in courselist].index(sectionthree[i])
        courselist[idx].section_count = 3

def process_final_courselist():
    i = 0
    for i in range(len(courselist)):
        if(courselist[i].section_count == 2 and len(courselist[i].course_name.split(' ')) != 4):
            temp = courselist[i]
            courselist.remove(courselist[i])
            temp.course_name  = temp.course_name + ' ' + 'Section' + ' ' + '2'
            courselist.append(temp)
        elif(courselist[i].section_count == 3 and len(courselist[i].course_name.split(' ')) != 4):
            temp = courselist[i]
            courselist.remove(courselist[i])
            temp.course_name  = temp.course_name + ' ' + 'Section' + ' ' + '3'
            courselist.append(temp)

process_course()
process_teacher()
process_section()
process_final_courselist()
