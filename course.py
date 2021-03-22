import datetime
import requests
import json

baseHandbookURL = "https://www.handbook.unsw.edu.au"

baseAPIURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_psubject%20+unsw_psubject.studyLevelURL:undergraduate%20+unsw_psubject.implementationYear:"

subjectCodeURL = "%20+unsw_psubject.code:"

def getCourseData(courseJSON):

    course = {
        'courseName' : courseJSON['description'],
        'courseCode': courseJSON['academic_item_code'],
        'handbookURL' : courseJSON['academic_item_url'],
    }

    courseURL = baseAPIURL + str(datetime.datetime.now().year) + "%20+unsw_psubject.code:" + course['courseCode']
    course['apiURL'] = courseURL
    coursePage = requests.get(courseURL)

    print(course['courseName'])
    print(coursePage)
    courseJSON = coursePage.json()['contentlets'][0]

    f = open("courseJSON.txt", "w")
    f.write(json.dumps(courseJSON))
    f.close()

    unitOffering = json.loads(courseJSON['data'])['offering_detail']['offering_terms']

    # print(json.loads(courseJSON['data'])['enrolment_rules'])

    requisiteString = ''

    try:
        # If the course has any pre requisites
        requisiteString = json.loads(courseJSON['data'])['enrolment_rules'][0]['description']
        #for word in requisiteString.split(' '):
        #    print(word)
        print(requisiteString)

    except:
        course['requisites'] = []

    

    print(unitOffering)
    return course