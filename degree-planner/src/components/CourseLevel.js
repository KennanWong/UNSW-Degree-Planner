import  { useEffect, useState } from 'react'

import Courses from './Courses'

const CourseLevel = ({courseLevel}) => {
    const [courses, setCourses] = useState([])

    // Delete course
    const deleteCourse = (courseCode) => {
        setCourses(courses.filter((course) => course.courseCode !== courseCode))
    }
    
    useEffect(() => {
        getCourses({courseLevel})
    }, [setCourses])
    
    async function getCourses({courseLevel}) {
        const payload = {searchString: courseLevel, field: 'level'};
        const response = await fetch('/search_course_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        response.json().then(data => {
          setCourses(data.courses)
        })
    }
    

    return (
        <div>
            <h2>{courseLevel}</h2>
            {courses.length > 0 ? <Courses courses = {courses} onDelete = {deleteCourse}/>: 'No Courses to show'}
        </div>
    )
}

export default CourseLevel
