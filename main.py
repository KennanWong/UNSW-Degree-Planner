#from selenium import webdriver
import requests
import json
import course

def main():
    
    baseURL = "https://www.handbook.unsw.edu.au"
    
    specialisationURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_paos%20+unsw_paos.studyLevelURL:undergraduate%20+unsw_paos.implementationYear:"
    genericURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_pcourse%20+unsw_pcourse.studyLevelURL:undergraduate%20+unsw_pcourse.implementationYear:"

    courseCode = input("Enter your course code: ")

    
    implentationYear = input("Enter the year you started: ")

    courseURL = ''

    if courseCode.isnumeric():
        courseURL = genericURL + implentationYear + "%20+unsw_pcourse.code:" + courseCode
    else :
        courseURL = specialisationURL + implentationYear + "%20+unsw_paos.code:" + courseCode
    
    
    degreePage = requests.get(courseURL)
    print("Searching url: " + courseURL)
   
    degreeJSON = degreePage.json()['contentlets'][0]

    curriculumStructure = json.loads(degreeJSON['CurriculumStructure'])

    noUOC = curriculumStructure['credit_points']
    
    #print("num uoc = " + noUOC)

    
    #for key in json.loads(courseJSON['data']).keys():
    #    print(key)

    
    f = open("container.txt", "w")
    f.write(json.dumps(curriculumStructure['container'][0]))
    f.close()

    dataJSON = json.loads(degreeJSON['data'])
    courseJSON = curriculumStructure['container'][0]['container']
    degreeName = dataJSON['title']
    degree = {
        'degreeName' : degreeName,
        'degreeCode' : courseCode,
        'implementationYear': implentationYear,
        'handbookURL' : courseURL,
        'courses' :[]
    }

    print(json.dumps(degree))

    for degreeLevel in courseJSON:
        level = degreeLevel['title']
        order = degreeLevel['order']
        courses = degreeLevel['relationship']
        for courseJSON in courses:
            newCours = {}
            try :
                newCourse = course.getCourseData(courseJSON)
                newCourse['order'] = order
                newCourse['Level'] = level
            except:
                print("Course no longer in use")


if __name__ == "__main__":
    main()