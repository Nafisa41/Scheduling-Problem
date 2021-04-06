#slot er array ta
#dictionary for teacher
#dictionary for timeslot
#dictionary for year 
#12 ta theke kono 3 credit class start korte parbo na same goes for 4 ta
import datetime
import numpy 
from dataprocess import Teacher
from dataprocess import Course
from dataprocess import courselist
from dataprocess import teacherlist
from dataprocess import process_class_cnt
diction_day = {}
timeslots = []
course_cnt = numpy.full((1, 50), 0)
free = numpy.full((6, 6,80), 0)
teacher_slot = numpy.full((40, 80), 0)
valid_time = [
    datetime.datetime.strptime('08:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('09:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('09:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('10:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('10:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('11:00 AM', '%I:%M %p'),
    datetime.datetime.strptime('11:30 AM', '%I:%M %p'),
    datetime.datetime.strptime('12:00 PM', '%I:%M %p'),
    datetime.datetime.strptime('12:30 PM', '%I:%M %p'),
    datetime.datetime.strptime('02:00 PM', '%I:%M %p'),
    datetime.datetime.strptime('02:30 PM', '%I:%M %p'),
    datetime.datetime.strptime('03:00 PM', '%I:%M %p'),
    datetime.datetime.strptime('03:30 PM', '%I:%M %p'),
    datetime.datetime.strptime('04:00 PM', '%I:%M %p'),
    datetime.datetime.strptime('04:30 PM', '%I:%M %p'),
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
            
    
#ektu dekhte hobe abar
def process_teacher_wanttime(teacher_idx, time_idx):
    day_idx = diction_day[timeslots[time_idx][0]]
    timelist = teacherlist[teacher_idx].valid_time[day_idx]
    i = 0
    for i in range(len(timelist)):
        if(timelist[i][0] >= timeslots[time_idx][1] and timelist[i][1] <= timeslots[time_idx][1]):
            return True
    return False

def check_time(idx, i): # see if we can finish the class if we start now.
    if(timeslots[idx][1] == datetime.datetime.strptime('12:30 PM', '%I:%M %p') or timeslots[idx][1] == datetime.datetime.strptime('04:30 PM', '%I:%M %p')):
        return False
    if(courselist[i].lab_course == False and courselist[i].credit == 3):
        if(timeslots[idx][1] == datetime.datetime.strptime('12:00 AM', '%I:%M %p') or timeslots[idx][1] ==  datetime.datetime.strptime('04:00 PM', '%I:%M %p')):
            return False
    if(courselist[i].lab_course == True):
        if( timeslots[idx][1] == datetime.datetime.strptime('08:30 AM', '%I:%M %p') or
            timeslots[idx][1] == datetime.datetime.strptime('09:00 AM', '%I:%M %p') or
            timeslots[idx][1] == datetime.datetime.strptime('09:30 AM', '%I:%M %p') or
            timeslots[idx][1] == datetime.datetime.strptime('10:00 AM', '%I:%M %p') or
            timeslots[idx][1] == datetime.datetime.strptime('02:00 PM', '%I:%M %p')):
            return True
        else:
            return False
    return True


def update_free(course_idx, year, section, time_idx, keep):
    day = timeslots[time_idx][0] #sunday or monday
    crdt = courselist[course_idx].credit
    loopcnt = 0
    if(courselist[course_idx].lab_course == True):
        loopcnt = 6
    else:
        if(crdt == 2) loopcnt = 2
        else loopcnt = 3 
    i = time_idx
    val = time_idx + loopcnt
    for i in range(val)):
        free[year][section][i] = keep

def update_teacherslot(teacher_idx, time_idx, keep):
    day = timeslots[time_idx][0] #sunday or monday
    crdt = courselist[course_idx].credit
    loopcnt = 0
    if(courselist[course_idx].lab_course == True):
        loopcnt = 6
    else:
        if(crdt == 2) loopcnt = 2
        else loopcnt = 3 
    i = time_idx
    val = time_idx + loopcnt
    for i in range(val)):
        free[teacher_idx][i] = keep


process_timeslot_list()
process_diction_day()

def main_algo(idx):
    #base case
    if(idx == 75):
        return
    i = 0
    for i in range(len(courselist)):
        #pichoner slot gulao dekhte hobe
        str = courselist[i].course_name.split(' ')
        year = int(str[1][0])
        section = 0
        if(courselist[i].lab_course == True):
            section = int(str[3][0])
        tot_class = course_cnt[i]
        if(free[year][section][idx] == 0 and tot_class < courselist[i].class_cnt and check_time(idx, i) == True):
            for j in range(len(teacherlist)):
                want_course = False
                want_time = False
                free_time = False
                if(courselist[i].course_name in teacherlist[j].assigned_courses):
                    want_course = True
                if(process_teacher_wanttime(j,idx)):
                    want_time = True
                if(teacher_slot[j][idx] == 0):
                    free_time = True
                if(want_course == True and want_time == True and free_time == True):
                    course_cnt[i] += 1
                    update_free(i, year, section, idx, 1)
                    update_teacherslot(j, idx, 1)
                    main_algo(idx + 1)
                    course_cnt[i] -= 1
                    update_free(i, year, section, idx, 0)
                    update_teacherslot(j, idx, 0)

                




    