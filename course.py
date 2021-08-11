import datetime
from os import error
import requests
import json

baseHandbookURL = "https://www.handbook.unsw.edu.au"

baseAPIURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_psubject%20+unsw_psubject.studyLevelURL:undergraduate%20+unsw_psubject.implementationYear:"

subjectCodeURL = "%20+unsw_psubject.code:"

coursesList = []


# course {
#     'courseName'
#     'courseCode'
#     'handbookURL'
#     'termOfferings': []
#     'apiURL'
#     'preRequisites' : []
#     'nextCourses': []

# }

# Creates a course dictionary from JSON
def formCourseDict(courseJSON):

    # try and find a course within coursesList
    course = {}
    courseCode = courseJSON['academic_item_code']
    course = searchCourseByField(courseCode, 'courseCode')
    if (not course):
        course = {
            'courseCode' : courseCode,
            'preRequisites': [],
            'nextCourses': []
        }
        print("created a new course dict")

    
    course['handbookURL'] = courseJSON['academic_item_url']
    course['courseName'] = courseJSON['description']
    
    courseURL = baseAPIURL + str(datetime.datetime.now().year) + "%20+unsw_psubject.code:" + course['courseCode']
    
    course['apiURL'] = courseURL
    coursePage = requests.get(courseURL)
    courseJSON = coursePage.json()['contentlets'][0]
    course['termOffering'] = json.loads(courseJSON['data'])['offering_detail']['offering_terms']
    requisiteString = ''
    course['preRequisites'] = []
    
    try:
        requisiteString = json.loads(courseJSON['data'])['enrolment_rules'][0]['description']
        parsePreReqString(requisiteString,course)
    except:
        print("no pre reqs")

    print(course)
    return course

# creates a preReqCourse dict and attaches the previous course to the pre reqcourse 
def createPreReq(preReqCode, course):
    preReqCourse = searchCourseByField(preReqCode, 'courseCode')
    if(not preReqCourse):
        print("could not find existing course")
        preReqCourse = {
            'courseCode': preReqCode,
            'nextCourses': []
        }
    
    preReqCourse['nextCourses'].append(course['courseCode'])
    coursesList.append(preReqCourse)
    print("added pre req course :" + preReqCode)
    


def getCoursesFromJSON(coursesJSON):
    for degreeLevel in coursesJSON:
        level = degreeLevel['title']
        order = degreeLevel['order']
        courses = degreeLevel['relationship']
        for courseJSON in courses:
            newCourse = {}
            try :
                newCourse = formCourseDict(courseJSON)
                newCourse['order'] = order
                newCourse['Level'] = level
                coursesList.append(newCourse)
                print("added a course")
            except:
                print("Course no longer in use")
            
    return coursesList
    
def searchCourseByField(searchString, field):
    print("searching course[" + field + "] = " + searchString)
    for course in coursesList:
        if course[field] == searchString:
            print("found existing course")
            return course
    print("could not find course")
    return False

# Parses pre req sring and adds it to the appropriate course
# Prequisites ordered as a list, if one of a few subjects need to be completed they will be grouped as a list
def parsePreReqString(preReqString, course):
    print("parsing prereqstring")
    preReqList = preReqString.split()
    print(preReqList)
    tempPreReq = []
    for i in preReqList:
        if (len(i) == 8):
            if (isCourseCode(i)):
                createPreReq(i,course)
                tempPreReq.append(i)
        elif (len(i) > 8):
            if (isCourseCode(i[0:8])):
                createPreReq(i[0:8], course)
                tempPreReq.append(i[0:8])
            elif (isCourseCode(i[1:9])):
                createPreReq(i[1:9], course)
                tempPreReq.append(i[1:9])
        if (i.lower() == 'and'):
            course['preRequisites'].append(tempPreReq)
            tempPreReq = []
    course['preRequisites'].append(tempPreReq)
    return

#checks if you can load up a url page for a course
def isCourseCode(courseCode):
    if (courseCode[4:8].isnumeric()):
        print(courseCode + " a real course")
        return True
    else:
        print("not a course")
        return False


def loadCourseListData(courses):
    coursesList = courses
    print("loaded course list")