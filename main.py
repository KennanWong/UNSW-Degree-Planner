#from selenium import webdriver
import os
import requests
import json
import course

degree = {}

def main():
    
    baseURL = "https://www.handbook.unsw.edu.au"
    
    specialisationURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_paos%20+unsw_paos.studyLevelURL:undergraduate%20+unsw_paos.implementationYear:"
    genericURL = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_pcourse%20+unsw_pcourse.studyLevelURL:undergraduate%20+unsw_pcourse.implementationYear:"

    degreeCode = input("Enter your course code: ")
    implementationYear = input("Enter the year you started: ")

    courseURL = ''

    #Check if we have a save for this specific degree and load it up

    degreeFileName = degreeCode+'_'+implementationYear

    if (os.path.isfile('./'+degreeFileName+'.json')):
        print("loading from save")
        degreeSave = open(degreeFileName+'.json', 'r')
        degree = json.load(degreeSave)
        course.loadCourseListData(degree['courses'])
        print("Finished loading save")

    else:
        if degreeCode.isnumeric():
            courseURL = genericURL + implementationYear + "%20+unsw_pcourse.code:" + degreeCode
        else :
            courseURL = specialisationURL + implementationYear + "%20+unsw_paos.code:" + degreeCode
        
        
        degreePage = requests.get(courseURL)
        print("Searching url: " + courseURL)
    
        degreeJSON = degreePage.json()['contentlets'][0]
        curriculumStructure = json.loads(degreeJSON['CurriculumStructure'])
        noUOC = curriculumStructure['credit_points']
        f = open("container.txt", "w")
        f.write(json.dumps(curriculumStructure['container'][0]))
        f.close()

        dataJSON = json.loads(degreeJSON['data'])
        coursesJSON = curriculumStructure['container'][0]['container']
        degreeName = dataJSON['title']
        degree = {
            'degreeName' : degreeName,
            'degreeCode' : degreeCode,
            'implementationYear': implementationYear,
            'handbookURL' : courseURL,
            'courses' :[]
        }

        print(json.dumps(degree))



        degree['courses'] = course.getCoursesFromJSON(coursesJSON)

        with open(degreeFileName+'.json', 'w') as json_file:
            json.dump(degree, json_file)
    

if __name__ == "__main__":
    main()