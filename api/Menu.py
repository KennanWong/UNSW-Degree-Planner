from flask import Blueprint, jsonify, request

from . import Degree 
from . import Course 

SUCESS = '200'

main = Blueprint('main', __name__)


@main.route('/add_degree', methods = ['POST'])
def add_degree():
    payload = request.get_json()

    print(payload)

    ret = Degree.initialiseDegree(payload['degreeCode'], payload['implementationYear'])

    return ret

# Figure out how to have this unique to degree i.e MTRNAH2019/courses
@main.route('/list_core_courses', methods = ['GET'])
def list_core_courses():
    coursesList = Course.searchCoursesByField(Course.getCoursesList(),'Core', 'level')
    courses = []

    for course in coursesList:
        courses.append({'courseCode': course['courseCode']})

    return jsonify({'courses':courses})

@main.route('/get_degree', methods = ['GET'])
def get_degree():
    return jsonify({'degreeCode': Degree.getDegreeCode(), 'year': Degree.getYear()})

@main.route('/is_degree_loaded', methods = ['GET'])
def is_degree_loaded():
    return jsonify({'degreeLoaded': Degree.isDegreeLoaded()})


@main.route('/set_degree_loaded', methods = ['POST'])
def set_degree_loaded():
    payload = request.get_json()
    Degree.setDegreeLoaded(payload['isDegreeLoaded'])
    return SUCESS


@main.route('/get_course_categories', methods = ['GET'])
def get_course_categories():
    levels = Course.getCategories(Course.getCoursesList(), 'level')
    
    for level in levels:
        if 'Core' not in level:
            levels.remove(level)

    print(levels)
    return jsonify({'courseLevels': levels})

@main.route('/search_course_list', methods = ['POST'])
def search_course_list():
    payload = request.get_json()
    print(payload)
    ret = Course.searchCoursesByField(Course.getCoursesList(), payload['searchString'], payload['field'])

    return jsonify({'courses': ret})

