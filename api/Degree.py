#from selenium import webdriver
import os
import requests
import json
import sqlite3

from . import Course 

degreeJSON = {}
degreeLoaded = 0

# for debugging purposes
disableLoading = False
'''
degreeJSON = {
    'degreeName' : degreeName,
    'degreeCode' : degreeCode,
    'implementationYear': implementationYear,
    'handbookURL' : courseURL,
    'courses' :[]
}
'''



def initialiseDegree(degreeCode, implementationYear):
    global degreeJSON, degreeLoaded, disableLoading
    
    baseURL = "https://www.handbook.unsw.edu.au"
    
    specialisationURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_paos%20+unsw_paos.studyLevelURL:undergraduate%20+unsw_paos.implementationYear:"
    genericURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_pcourse%20+unsw_pcourse.studyLevelURL:undergraduate%20+unsw_pcourse.implementationYear:"


    if (not implementationYear.isnumeric()):
        print("Invalid implementation year given.")
        return 

    courseURL = ''

    #Check if we have a save for this specific degree and load it up

    degreeFileName = degreeCode+'_'+implementationYear

    if (os.path.isfile(degreeFileName+'.json') and not disableLoading):
        print("loading from save")
        degreeSave = open(degreeFileName+'.json', 'r')
        degreeJSON = json.load(degreeSave)
        Course.loadCourseListData(degreeJSON['courses'])
        print("Finished loading save")
        print(degreeJSON['handbookURL'])
    else:
        if degreeCode.isnumeric():
            handbookURL = genericURL + implementationYear + "%20+unsw_pcourse.code:" + degreeCode
        else :
            handbookURL = specialisationURL + implementationYear + "%20+unsw_paos.code:" + degreeCode
        
        degreePage = requests.get(handbookURL)
        print("Searching url: " + handbookURL)
    
        degreeJSON = degreePage.json()['contentlets'][0]
        curriculumStructure = json.loads(degreeJSON['CurriculumStructure'])
        noUOC = curriculumStructure['credit_points']

        dataJSON = json.loads(degreeJSON['data'])
        coursesJSON = curriculumStructure['container'][0]['container']
        degreeName = dataJSON['title']
        degreeJSON = {
            'degreeName' : degreeName,
            'degreeCode' : degreeCode,
            'implementationYear': implementationYear,
            'handbookURL' : handbookURL,
            'UOC': noUOC,
            'courses' :[]
        }
        print(json.dumps(degreeJSON))

            
        ret = Course.getCoursesFromJSON(coursesJSON)

        degreeJSON['courses'] = ret['coursesList']

        print("Errors: " )
        print(ret['errors'])

        with open(degreeFileName+'.json', 'w') as json_file:
            json.dump(degreeJSON, json_file)
    
    print("Finished initilaising degree")
    degreeLoaded += 1
    return 'Done'

def getDegreeJSON():
    return degreeJSON
    
def getDegreeCode():
    return degreeJSON['degreeCode']

def getYear():
    return degreeJSON['implementationYear']

def isDegreeLoaded():
    print('DegreeLoaded '+ str(degreeLoaded))
    if degreeLoaded == 0:
        return False
    else:
        return True

def setDegreeLoaded(state):
    global degreeLoaded
    degreeLoaded = state
    if (state == 0):
        Course.clearCourseList()