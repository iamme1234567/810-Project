# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 17:44:53 2016

@author: yujiezhong
"""

import sys
from collections import defaultdict
from prettytable import PrettyTable


NAME = "name"
MAJOR = "major"


def find_error_input(msg):
    inp = input(msg)

    try:
        file = open(inp, 'r')
    except (FileNotFoundError, IOError):
        if inp.strip() == '':
            errmsg = 'File name cannot be empty!'
        else:
            errmsg = 'File cannot be found!: ' + inp

        print(errmsg)
        sys.exit(1)
    
    return file    


def test(did_pass):
    ''' print the result of a test '''
    linenum = sys._getframe(1).f_lineno # get the caller's line number
    if did_pass:
        msg = 'Test at line {0} ok.'.format(linenum)
    else:
        msg = 'Test at line {0} FAILED.'.format(linenum)
    print(msg)
    

def read_separated_file(file):
    '''read a file that the data is separated by '|', and returan a list of data pairs'''
    C_NM_sep = list()
    
    for line in file.readlines():
        items = [item for item in line.strip().split('|')]
        
        if len(items) < 2:
           print("There is an invalid data in line!") 
           continue
        
        C_NM_sep.append((items[0],items[1:]))
    
    return C_NM_sep
       

def read_student():
    '''read the student file and store the info into a dictionary'''
    s = find_error_input("Enter the student file name: ")
    studentdd = defaultdict(lambda:defaultdict(str))
    
    for data in read_separated_file(s):
        cwid = data[0]
        nm = data[1]
        
        if len(data) < 2:
            print("The cwid {} cannot be found".format(cwid))
            continue
        
        studentdd[cwid][NAME] = nm[0]
        studentdd[cwid][MAJOR] = nm[1]
    
    s.close()
    return studentdd


def read_required_courses():
    '''read the required courses file and store the data into a dictionary'''
    rc = find_error_input("Enter the required course file name: ")
    rcd = defaultdict(set)
    
    for data in read_separated_file(rc):
        major = data[0]
        course = data[1]
        
        if len(course) == 0:
            print("The major {} cannot be found".format(major))
            continue
        
        for cors in course:
            rcd[major].add(cors)
            
    rc.close()
    return rcd


def read_grades():
    '''read the grades file and store the data into a dictionary'''
    g = find_error_input("Enter the grades file name: ")
    gradesdd = defaultdict(lambda:defaultdict(str))
    
    for data in read_separated_file(g):
        cwid = data[0]
        clg = data[1]
        
        if len(clg) < 2 and len(clg) == 1:
            print("The student {} has no grades on course {}".format(cwid,clg[0]))
            continue
        
        gradesdd[cwid][clg[0]] = clg[1]
        
    g.close()
    return gradesdd


def is_course_passed(grade):
    return True

    
def student_report(students, courses, grades):
    '''Summarize the info of students'''
    report = list()
    
    for cwid, val in students.items():
        major = val[MAJOR]

        completed = set(c for c, g in grades[cwid].items() if is_course_passed(g))
        
        unfinish = sorted(rest for rest in courses[major].difference(completed))
        
        name = val[NAME]

        report.append([name, cwid, major, unfinish])

    return report
    

def main():
    '''generate a table for the student info and report'''
    head = ['Name', 'CWID', 'Major', 'Remaining classes']
    table = PrettyTable(head)
    table.align[head[0]] = '|'
    table.padding_width = 1
    
    s,rc,g = read_student(),read_required_courses(),read_grades()
    
    rpt = student_report(s, rc, g)
    
    for item in rpt:
        
        table.add_row(item)
    
    print(table)
    

def test_suite():
    test(is_course_passed(0)==True)
test_suite()
main()
