import  {useState } from 'react'

import CourseLevel from './CourseLevel';

const CourseLevels = ({courseLevels}) => {
    return (
        <div>
            {courseLevels.map((courseLevel => (
                <CourseLevel key = {courseLevel} courseLevel = {courseLevel}/>
            )))}
        </div>
    )
}

export default CourseLevels
