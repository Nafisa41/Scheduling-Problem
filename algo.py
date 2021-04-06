#slot er array ta
#dictionary for teacher
#dictionary for timeslot
#dictionary for year 
import datetime
import numpy 
from dataprocess import Teacher
from dataprocess import Course
from dataprocess import courselist
from dataprocess import teacherlist
diction_teacher = {}
diction_course = {}
timeslots = []
course_cnt = numpy.full((1, 50), 0)
free = numpy.full((6, 6,80), 0)
teacher_slot = numpy.full((40, 80), 0)
valid_time = [
    datetime.datetime.strptime('08:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('09:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('09:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('10:00 PM', '%I:%M %p'),
    datetime.datetime.strptime('10:30 PM', '%I:%M %p'),
    datetime.datetime.strptime('11:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('11:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('12:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('01:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('01:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('02:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('02:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('03:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('03:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('04:00 AM', '%I:%M %p'),
    ]

def process_timeslot_list():
    i = 0
    for i in range(5):
        timeslots.append(valid_time)

def process_diction_course():
    i = 0
    for i in range(len(courselist)):
        diction_course[courselist[i].course_name] = i

def process_diction_teacher():
    i = 0
    for i in range(len(teacherlist)):
        diction_teacher[teacherlist[i].teacher_initial] = i

def process_year_free(course, idx):
    str = course.course_name.split(' ')
    year = int(str[1][0])
    section = int(str[4][0])
    if(course.lab_course == False):
        if(course.credit == 2.0):
            if(idx - 1 >= 0):
                if(free[year][0][idx] == 0 and free[year][0][idx - 1] == 0):
                    return True
            else:
                if(free[year][0][idx] == 0)
                    return True
        if(course.credit == 3.0):
            if(idx - 1 >= and idx - 2 >= 0):
                if(free[year][0][idx] == 0 and free[year][[0][idx - 1] == 0 and free[year][0][idx - 2] == 0):
                    return True
            elif(idx - 1 >= 0):
                if(free[year][0][idx] == 0 and free[year][0][idx - 1] == 0):
                    return True
            else:
                if(free[year][0][idx] == 0)
                    return True

    if(course.lab_course == True):
        if(free[year][section][idx] == 0):
            return True
    return False

def process_teacher_free(Teacher, idx):
    if(teacher_slot[diction_teacher[Teacher.teacher_initial]][idx] == 0):
        return True
    else:
        return False


def process_teacher_free_time(Teacher, idx):


process_timeslot_list()
process_diction_course()
process_diction_teacher()

def main_algo(idx):
    i = 0
    for i in range(len(courselist)):
        #pichoner slot gulao dekhte hobe
        is_free = process_year_free(courselist[i], idx)
        tot_class = course_cnt[courselist[i].course_name]
        if(is_free == True andd tot_class < courselist[i].class_cnt):
            
            for j in range(len(teacherlist)):
                teacher_free = process_teacher_free(teacherlist[j], idx)
                want_course = False
                if(courselist[i].course_name in teacherlist[j].assigned_courses):
                    want_course = True
                

                




    