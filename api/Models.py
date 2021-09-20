import json

from . import helper_functions


class Course:
    def __init__(self, courseCode, courseName, termOfferings, preRequisites, relationship,
                 relatedCourses, order, level, creditpoints):
        self.courseCode = courseCode
        self.courseName = courseName
        self.termOfferings = termOfferings
        self.preRequisites = preRequisites
        self.relationship = relationship
        self.relatedCourses = relatedCourses
        self.order = order
        self.level = level
        self.creditPoints = creditpoints
    
    def getTermOfferingsString(self):
        return helper_functions.listToString(self.termOfferings)

    def getPreRequisiteString(self):
        return helper_functions.listToString(self.preRequisites)
    
    def getRelatedCoursesString(self):
        return helper_functions.listToString(self.relatedCourses)

    def asJson(self):
        return json.dumps(self.__dict__)


class Degree:
    def __init__(self, degreeCode, degreeName, implementationYear, coursesList, noUOC):
        self.degreeCode = degreeCode
        self.degreeName = degreeName
        self.implementationYear = implementationYear
        self.coursesList = coursesList
        self.noUOC = noUOC
