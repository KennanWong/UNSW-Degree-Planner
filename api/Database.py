from os import error
from . import models
import sqlite3

def createConnection(dbName):
    """ create a databse connection to the SQLite database specified
        by dbName

        :param dbName: database file
        :return Connection object or None
    """

    try:
        conn = sqlite3.connect(dbName+'.db')
    except error as e:
        print(e)
    
    return conn

def createDegreesDB(dbName):
    """ Creates the degree database with a given dbName

        :param dbName
        :return

    """
    try:
        conn = sqlite3.connect('Degrees.db')
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS Degrees
                    degreeCode TEXT,
                    degreeName TEXT,
                    implementationYear TEXT,
                    courseDBName TEXT,
                    """)
    except error as e:
        print(e)

    return

def insertNewDegree(degree):
    conn = sqlite3.connect('Degrees.db')
    c = conn.cursor()
    c.execute("INSERT INTO Degrees VALUES (?, ?, ?, ?)", (
                degree.degreeCode, degree.degreeName, degree.implementationYear, degree.courseDBName
                ))

def createCourseDB(dbName):
    """ Creates the courses database with a given dbName

        :param dbName: database name
        :return 
    """
    try:
        conn = sqlite3.connect(dbName+'.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Courses (
                    courseCode TEXT,
                    courseName TEXT,
                    termOfferings TEXT,
                    preRequisites TEXT,
                    relationship TEXT,
                    relatedCourses TEXT,
                    order INTEGER,
                    level TEXT,
                    creditPoints INTEGER
                    )""")

    except error as e:
        print(e)
    return 

def insertCourseToDB(dbName, course):
    """ Given a DBName, insert the course into it

        :param  String dbName: database name
                Course course: course to be added
        :return     
    """
    c = getCursorFromDB(dbName)
    c.execute("INSERT INTO Courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (course.CourseCode, course.courseName, course.getTermOfferingsString, course.getPreRequisiteString, 
                course.relationship, course.getRelatedCoursesString, course.order, course.level, course.creditPoints 
                ))



def getCursorFromDB(dbName):
    conn = sqlite3.connect(dbName+'.db')
    return conn.cursor