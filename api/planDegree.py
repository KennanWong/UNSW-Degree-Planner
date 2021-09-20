import json
import math

from . import Course

plan = []

NUM_TERMS = 3
AVERAGE_UOC = 6
NUM_COURSE_PER_YEAR = 8

def initialisePlan(degree):
    global plan
    numYears = math.ceil(int(degree['UOC'])/(AVERAGE_UOC * NUM_COURSE_PER_YEAR))
    for i in range(1,numYears + 1):
        plan.append(newYear(i))

    for year in plan:
        print (year)

def newYear(yearNumber):
    newYear = {
        'year': yearNumber,
        'terms': []
    }
    for i in range(1, NUM_TERMS+1):
        newYear['terms'].append(newTerm(i))
    
    return newYear

def newTerm(termNumber):
    newTerm = {
        'term': termNumber,
        'courses': []
    }
    return newTerm


def addCourseToTerm(term, year, courseCode):
    global plan
    course = Course.searchCoursesByField(Course.getCoursesList(), courseCode, 'courseCode')
    term = plan[year-1]['terms'][term-1]

    if (isValidCourse(courseCode, term, year)):
        term['courses'].append(courseCode)
        return 
    else: 
        return 'Pre reqs not met'


def isValidCourse(courseCode, selectedTerm, selectedYear):
    course = Course.searchCoursesByField(Course.getCoursesList(), courseCode, 'courseCode')
    print(course)
    preReqs = course['preRequisites']
    if not checkPreReqMet(courseCode, selectedTerm, selectedYear, preReqs):
        return False
    
    ret = searchForCourseInPlan(courseCode)

    if ret is not None:
        global plan
        plan[ret[0]-1]['terms'][ret[1]-1]['courses'].remove(courseCode)
    
    return True

    

def displayDegreePlan():
    for year in plan:
        print("YEAR "+ str(year['year']))
        print('-----------------------------------')
        for term in year['terms']:
            print('Term '+ str(term['term']) + str(term['courses']))
        print('     ')

def checkPreReqMet(courseCode, selectedTerm, selectedYear, preReqs):
    if len(preReqs) == 0:
        return True

    for year in plan:
        for term in year['terms']:
            if (term['term'] is selectedTerm and year['year'] is selectedYear ):
                break
            else :
                for preReq in preReqs:
                    if isinstance(preReq, list):
                        for item in preReq:
                            if item in term['courses']:
                                preReqs.remove(preReq)
                    if preReq in term['courses']:
                        preReqs.remove(preReq)
    
    if len(preReqs) == 0:
        return True

    else:
        return False

def searchForCourseInPlan(courseCode):
    global plan
    for year in plan:
        for term in year['terms']:
            if courseCode in term['courses']:
                return  year['year'], term['term'] 

    return