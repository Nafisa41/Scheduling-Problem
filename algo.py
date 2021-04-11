import datetime
import numpy 
from dataprocess import Teacher
from dataprocess import Course
from dataprocess import courselist
from dataprocess import teacherlist
from dataprocess import teacher_course_mp
year_time = [[],[],[],[],[]] #start time end time day and section
teacher_name = []
teacher_time = []
diction_day = {}
timeslots = []
course_cnt = numpy.full((60), 0)
valid_time = [
    datetime.datetime.strptime('08:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('10:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('11:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('02:00 PM', '%I:%M %p'),
    datetime.datetime.strptime('03:30 PM', '%I:%M %p'),
    ]

def process_diction_day():
    diction_day['Sunday'] = 0
    diction_day['Monday'] = 1
    diction_day['Tuesday'] = 2
    diction_day['Wednesday'] = 3
    diction_day['Thursday'] = 4

def process_timeslot_list():
    days = []
    days.append('Sunday')
    days.append('Monday')
    days.append('Tuesday')
    days.append('Wednesday')
    days.append('Thursday')
    i = 0
    j = 0
    for i in range(5):
        for j in range(len(valid_time)):
            timeslots.append((days[i], valid_time[j]))

def process_teacher_time():
    for i in range(len(teacherlist)):
        teacher_time.append([])

def read_course_teacher_free(course_idx, teacher_idx, time_idx, id): #id 0 for course and 1 for teacher
    flag = True
    day = timeslots[time_idx][0]
    start_time = timeslots[time_idx][1]
    end_time = timeslots[time_idx][1] + courselist[course_idx].duration
    if(end_time >  datetime.datetime.strptime('05:00 PM', '%I:%M %p') or end_time ==  datetime.datetime.strptime('02:30 PM', '%I:%M %p')):
        return False
    list_idx = 0
    temp_list = []
    if(id == 0):
        temp_list = year_time
        list_idx = courselist[course_idx].course_year
    else:
        temp_list = teacher_time
        list_idx = teacher_idx
    for i in range(len(temp_list[list_idx])):
        if(temp_list[list_idx][i][2] != day):
            continue
        st = temp_list[list_idx][i][0]
        et = temp_list[list_idx][i][1]
        if((start_time >= st and start_time <= et) or (end_time >= st and end_time <= et)):
            flag = False
    return flag

def teacher_wanttime(teacher_idx, time_idx):
    day_idx = diction_day[timeslots[time_idx][0]]
    timelist = teacherlist[teacher_idx].valid_time[day_idx]
    i = 0
    for i in range(len(timelist)):
        if(timelist[i][0] >= timeslots[time_idx][1] and timelist[i][1] <= timeslots[time_idx][1]):
            return True
    return False

def read_course_cnt(course_idx):
    if(course_cnt[course_idx] >= courselist[course_idx].class_cnt):
        return False
    else:
        return True
    
def find_teacher_idx(teacher_name):
    for i in range(len(teacherlist)):
        if(teacherlist[i].teacher_initial == teacher_name):
            return i

def update_course_free(course_idx, time_idx, op):
    year = courselist[course_idx].course_year
    templist = [[],[],[],[]]
    templist[0] = timeslots[time_idx][1]
    templist[1] = timeslots[time_idx][1] + courselist[course_idx].duration
    templist[2] = timeslots[time_idx][0]
    templist[3] = courselist[course_idx].course_name
    if(op == "append"):
        year_time[year].append(templist)
    else:
        year_time[year].remove(templist)

def update_teacher_free(teacher_idx, time_idx, course_idx, op):
    templist = []
    templist = [[],[],[],[]]
    templist[0] = timeslots[time_idx][1]
    templist[1] = timeslots[time_idx][1] + courselist[course_idx].duration
    templist[2] = timeslots[time_idx][0]
    templist[3] = courselist[course_idx].course_name
    if(op == "append"):
        teacher_time[teacher_idx].append(templist)
    else:
        teacher_time[teacher_idx].remove(templist)

def udpate_course_cnt(course_idx, val):
    course_cnt[course_idx] = course_cnt[course_idx] + val

def func(idx):
    if(idx == 25):
        print(teacher_name)
        return
    for i in range(len(courselist)):
        teacher_idx = find_teacher_idx(teacher_course_mp[courselist[i].course_name])
        year_free = read_course_teacher_free(i, teacher_idx, idx, 0)
        teacher_free = read_course_teacher_free(i, teacher_idx, idx, 1)
        if(year_free == True and teacher_free == True and read_course_cnt(i) == True):
            update_course_free(i,idx,"append")
            update_teacher_free(teacher_idx, idx,i,"append")
            udpate_course_cnt(i, 1)
            teacher_name.append(teacherlist[teacher_idx].teacher_initial)
            func(idx + 1)
            update_course_free(i,idx,"remove")
            update_teacher_free(teacher_idx, idx,i,"remove")
            udpate_course_cnt(i, -1)
            teacher_name.append(teacherlist[teacher_idx].teacher_initial)

process_diction_day()
process_timeslot_list()
process_teacher_time()
func(0)