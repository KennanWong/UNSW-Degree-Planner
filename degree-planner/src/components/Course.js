import { FaTimes } from 'react-icons/fa'

const Course = ({course, onDelete}) => {


    return (
        <div className='course'>
            <h3>
                {course.courseCode}
                <FaTimes 
                    style = { {color:'black', cursor: 'pointer'}}
                    onClick = {() => onDelete(course.courseCode)}    
                />
            </h3>
        </div>
    )
}

export default Course
