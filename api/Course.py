import datetime
from os import error
import requests
import json
import sqlite3



baseHandbookURL = "https://www.handbook.unsw.edu.au"

baseAPIURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_psubject%20+unsw_psubject.studyLevelURL:undergraduate%20+unsw_psubject.implementationYear:"

subjectCodeURL = "%20+unsw_psubject.code:"

coursesList  = []


# course {
#     'courseName'
#     'courseCode'
#     'termOfferings': []
#     'preRequisites' : []
#     'nextCourses': []
#     'relationship':               'AND' or 'OR' to show if we need to do this or we need to this course or another
#     'relatedCourse':              the other course we may need to complete
#     'level'

# }

#Given the raw courseJSON data and creates the coursesList
def getCoursesFromJSON(coursesJSON):
    
    global coursesList
    error = []

    for degreeLevel in coursesJSON:
        level = degreeLevel['title']
        order = degreeLevel['order']
        courses = degreeLevel['relationship']
        for courseJSON in courses:
            try :  
                newCourse = formCourseDict(courseJSON)
                newCourse['order'] = order
                newCourse['level'] = level
                coursesList.append(newCourse)
            except:
                error.append(courseJSON['academic_item_code'])
        
        # Process courses in which one of the following must be taken
        
        containers = degreeLevel['container']
        for container in containers:
            # Hold onto the options to link the courses
            
            tmpOptions = []
            for cJSON in container['relationship']:
                try :
                    newCourse = formCourseDict(cJSON)
                    newCourse['order'] = order
                    newCourse['level'] = level
                    newCourse['relationship'] = 'OR'
                    tmpOptions.append(cJSON['academic_item_code'])
                    coursesList.append(newCourse)
                except:
                    error.append(cJSON['academic_item_code'])
                
            
            for i in tmpOptions:
                c_i = searchCoursesByField(coursesList, i, 'courseCode')
                print(c_i)
                for j in tmpOptions:
                    if i != j:
                        c_i['relatedCourses'].append(j) 
            
            
            
        

    ret = {
        'coursesList' : coursesList,
        'errors': error
    }
    return ret

# Creates a course dictionary from JSON
def formCourseDict(courseJSON):
    # try and find a course within coursesList
    global coursesList
    course = newEmptyCourse()
    courseCode = courseJSON['academic_item_code']
    course['courseCode'] = courseCode
    course['creditPoints'] = int(courseJSON['credit_points'])
    course['courseName'] = courseJSON['description']
    
    courseURL = baseAPIURL + str(datetime.datetime.now().year) + "%20+unsw_psubject.code:" + course['courseCode']

    coursePage = requests.get(courseURL)
    courseJSON = coursePage.json()['contentlets'][0]
    termOfferings = json.loads(courseJSON['data'])['offering_detail']['offering_terms']
    course['termOffering'] = parseTermOfferings(termOfferings)
    requisiteString = ''
    course['preRequisites'] = []
    
    try:
        requisiteString = json.loads(courseJSON['data'])['enrolment_rules'][0]['description']
        parsePreReqString(requisiteString,course)
    except:
        course['preRequisites'] = []

    print("finished forming courseDict for : "+ courseCode)
    return course

# creates a preReqCourse dict and attaches the previous course to the pre reqcourse 
def createPreReq(preReqCode, course):
    global coursesList
    
    preReqCourse = searchCoursesByField(coursesList, preReqCode, 'courseCode')
    
    if(not preReqCourse):
        preReqCourse = {
            'courseCode': preReqCode,
            'nextCourses': []
        }
        coursesList.append(preReqCourse)
    

    preReqCourse['nextCourses'].append(course['courseCode'])
    
# Parses pre req sring and adds it to the appropriate course
# Prequisites ordered as a list, if one of a few subjects need to be completed they will be grouped as a list
def parsePreReqString(preReqString, course):
    global coursesList
    preReqList = preReqString.split()
    tempPreReq = []
    exclusionsList = []
    exclusionsOn = False
    for i in preReqList:
        if (exclusionsOn == False):
            if (i.lower() == 'and'):
                course['preRequisites'].append(tempPreReq)
                tempPreReq = []
            elif ('exclusion' in i.lower()):
                exclusionsOn = True
            else:
                courseCode = getCourseCodeFromString(i)
                if (courseCode != False):
                    tempPreReq.append(courseCode)

        else:
            courseCode = getCourseCodeFromString(i)
            if (courseCode != False):
                exclusionsList.append(courseCode)

    course['preRequisites'].append(tempPreReq)
    course['exclusions'] = exclusionsList
    return

#checks if it s acourse code
def isCourseCode(courseCode):
    if (courseCode[4:8].isnumeric()):
        return True
    else:
        return False

def getCourseCodeFromString(string):
    if (len(string) == 8):
        if (isCourseCode(string)):
            return string
    else:
        if (isCourseCode(string[0:8])):
            return string[0:8]
        elif (isCourseCode(string[1:9])):
            return string[1:9]
        else:
            return False



def parseTermOfferings(termOfferings):
    global coursesList
    tempList = termOfferings.split()
    termList = []
    for item in tempList:
        if item.isnumeric() or item == 'Summer':
            termList.append(item)
    return termList


def loadCourseListData(courses):
    global coursesList
    coursesList = courses
    print("loaded course list")

# Given a list, searches for course[field] that matches, returns a list
def searchCoursesByField(courseList, searchString, field):
    retList = []
    for i in courseList:
        try:
            if searchString.upper() in i[field] or searchString in i[field]:
                retList.append(i)
        except:
            continue
    
    if len(retList) == 1:
        return retList[0]

    else:
        return retList

def getCategories(courseList, field):
    tmpList = []
    for i in courseList:
        try: 
            if i[field] not in tmpList:
                tmpList.append(i[field])
        except:
            continue

    
    return sorted(tmpList)

def newEmptyCourse():
    newCourse = {
        'courseCode': '',
        'courseName': '',
        'termOfferings': [],
        'preRequisites': [],
        'relationship': 'AND',
        'relatedCourses': [],
        'order': 0,
        'level': '',
        'creditPoints': 0
    }

    return newCourse

def saveToCoursesList(newCourse):
    new_course = Course(
        courseCode = newCourse['courseCode'], 
        courseName = newCourse['courseName'],
        termOfferings = helper_functions.listToString(newCourse['termOfferings']), 
        preRequisites = helper_functions.listToString(newCourse['preRequisites']),
        relationship = newCourse['relationship'],
        relatedCourses = helper_functions.listToString(newCourse['relatedCourses']),
        order = newCourse['order'],
        level = newCourse['level'],
        creditPoints = newCourse['creditPoints'])
    return

def getCoursesList():
    global coursesList
    return coursesList

def clearCourseList():
    global coursesList
    coursesList = []
        
        
        

