import  {useEffect, useState } from 'react'

import './App.css';
import Header from './components/Header'
import Button from './components/Button'
import Courses from './components/Courses'
import AddDegree from './components/AddDegree'
import CourseLevels from './components/CourseLevels';

function App() {
  const onClick = () => {
    console.log('Click')
  }

  const [courses, setCourses] = useState([])
  const [courseLevels, setCourseLevels] =useState([])
  
  useEffect(() => {
    getCourseLevels()
    
  }, [setCourseLevels])
  

  // Load Degree
  const addDegree = ({degreeCode, year}) => {
    loadDegree({degreeCode, year})
    getCourseLevels()
    getCoreCourses()
    
  }

  async function loadDegree({degreeCode, year}) {
    const payload = {degreeCode :degreeCode, implementationYear: year};
    const response = await fetch('/add_degree', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      console.log("Response worked")
    }
    getCourseLevels()
    
  }

  async function getCoreCourses() {
    const response = await fetch('/list_core_courses');
    response.json().then(data => {
      setCourses(data.courses)
    })
  }

  async function getCourseLevels() {
    const response = await fetch('/get_course_categories')
    response.json().then(data =>
      setCourseLevels(data.courseLevels))
    
  }
    

  const removeDegree = () => {
    (async() => {
      const payload = {isDegreeLoaded: 0};
      const response = await fetch('/set_degree_loaded', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
      });

      if (response.ok) {
          console.log("Response worked")
      }

      console.log("removed degree")
    })();
    setCourses([])
    setCourseLevels([])
    
  }

  // Delete course
  const deleteCourse = (courseCode) => {
    setCourses(courses.filter((course) => course.courseCode !== courseCode))
  }

  

  const display = 
  
    <div className="container">
        <Header/>
        <AddDegree onAdd = {addDegree} onRemove = {removeDegree}/>
        {courseLevels.length > 0 ?  <CourseLevels courseLevels = {courseLevels}/>: 'No Courses to show'}
        
    </div>

  
  return (
    display
  );
}

export default App;
