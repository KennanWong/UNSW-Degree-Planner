
import Degree
import Course
import planDegree
import Helper_functions

def main():
    initiliaseMenu()

def initiliaseMenu():
    while (True):
        print("Welcome to the UNSW Degree planner.")
        print("[1] Load up your Degree")
        print("[2] Search for a Course")
        print("[3] Search for core Courses")
        print("[4] List core Courses")
        print("[5] Initialise plan")
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
        elif command == '5':
            initiliasePlan()
        elif command == '!':
            exit()
        else:
            print("Invalid operation" )





# Loads a Degree, user is asked for Course code and implmentation year
def loadDegree():
    courseCode = input("Enter course code: ")
    implementationYear = input("Enter implmenetation year: ")
    Degree.initialiseDegree(courseCode, implementationYear)


# Search for a course
def searchCourse():
    if (Degree.isDegreeLoaded()):
        courseCode = input("Enter course code or subcourses you would like to search: ")
        searchResults = Course.searchCoursesByField(Course.coursesList, courseCode.upper(), 'courseCode')
        
        if isinstance(searchResults, list):
            searchResults = Helper_functions.sortList(searchResults, 'courseCode', False)

            for result in searchResults:
                print(result['courseCode'])
                print(result)
        else:
            print(searchResults)
    else:
        print("Degree has not been loaded to the program. Please load Degree") # Turn this to error.py

def searchCoursesAdv():
    if (Degree.isDegreeLoaded()):
        courseCode = input("Enter course code or subcourses you would like to search that are core courses: ")
        searchResults = Course.searchCoursesByField(Course.coursesList, courseCode.upper(), 'courseCode')
        
        if isinstance(searchResults, list):
            filteredResults = Course.searchCoursesByField(searchResults, 'Core', 'level')

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
    if (Degree.isDegreeLoaded()):
        levels = Course.getCategories(Course.coursesList, 'level')
        for i in levels:
            if 'Core' in i:
                print(i +':')
                ret = Course.searchCoursesByField(Course.coursesList, i, 'level')
                for j in ret:
                    print('\t'+j['courseCode'])

    else:
        print("Degree has not been loaded to the program. Please load Degree")


# Allow users plan their Degree by organising courses into terms and years
#   Will use another menu for organisation
def initiliasePlan():
    planDegree.initialisePlan(Degree.getDegreeJSON())

def exit():
    quit()


if __name__ == "__main__":
    main()