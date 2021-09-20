import  { useState } from 'react'

import Course from './Course'

const Courses = ({courses, onDelete}) => {

    return (
        <div>
            {courses.map((course) => ( 
                <Course key = {course.courseCode}  course = {course} onDelete = {onDelete}/>
            ))}
        </div>
    )
}

export default Courses
