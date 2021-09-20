import degree
import course
import helper_functions

def main():
    initiliaseMenu()

def initiliaseMenu():
    while (True):
        print("Welcome to the UNSW degree planner.")
        print("[1] Load up your degree")
        print("[2] Search for a course")
        print("[3] Search for core courses")
        print("[4] List core courses")
        print("[!] Exit the program")

        command = input("What would you want to do: ")

        if command == '1':
            loadDegree()
        elif command == '2':
            searchCourse()
        elif command == '3':
            searchCoursesAdv()
        elif command == '4':
            listCoreCourses()
        elif command == '!':
            exit()
        else:
            print("Invalid operation" )





# Loads a degree, user is asked for course code and implmentation year
def loadDegree():
    courseCode = input("Enter course code: ")
    implementationYear = input("Enter implmenetation year: ")
    degree.initialiseDegree(courseCode, implementationYear)


# Search for a course
def searchCourse():
    if (degree.isDegreeLoaded()):
        courseCode = input("Enter course code or subcourses you would like to search: ")
        searchResults = course.searchCoursesByField(course.coursesList, courseCode.upper(), 'courseCode')
        
        if isinstance(searchResults, list):
            searchResults = helper_functions.sortList(searchResults, 'courseCode', False)

            for result in searchResults:
                print(result['courseCode'])
                print(result)
        else:
            print(searchResults)
    else:
        print("Degree has not been loaded to the program. Please load Degree") # Turn this to error.py

def searchCoursesAdv():
    if (degree.isDegreeLoaded()):
        courseCode = input("Enter course code or subcourses you would like to search that are core courses: ")
        searchResults = course.searchCoursesByField(course.coursesList, courseCode.upper(), 'courseCode')
        
        if isinstance(searchResults, list):
            filteredResults = course.searchCoursesByField(searchResults, 'Core', 'level')

            if isinstance(filteredResults, list):
                for result in filteredResults:
                    print(result)
            else:
                print(filteredResults)
        else:
            print(searchResults['courseCode'])
                
    else:
        print("Degree has not been loaded to the program. Please load Degree")
    print 

def listCoreCourses():
    if (degree.isDegreeLoaded()):
        levels = course.getCategories(course.coursesList, 'level')
        for i in levels:
            if 'Core' in i:
                print(i +':')
                ret = course.searchCoursesByField(course.coursesList, i, 'level')
                for j in ret:
                    print('\t'+j['courseCode'])

    else:
        print("Degree has not been loaded to the program. Please load Degree")


# Allow users plan their degree by organising courses into terms and years
#   Will use another menu for organisation
def planDegree():
    print("Has not been implemented")

def exit():
    quit()


if __name__ == "__main__":
    main()