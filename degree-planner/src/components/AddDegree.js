import { useEffect, useState } from "react"
import { FaTimes } from 'react-icons/fa'


const AddDegree = ({onAdd, onRemove}) => {

    const [degreeCode, setDegreeCode] = useState('')
    const [year, setYear] = useState('')
    const [degreeLoaded, setDegreeLoaded] = useState('')

    const onClear = (e) => {
        onRemove()
        setDegreeCode('')
        setYear('')
        setDegreeLoaded('')
    }

    const onSubmit = (e) => {
        e.preventDefault()

        if(!degreeCode) {
            alert('Please add a Degree')
            return
        }

        if(!year) {
            alert('Please enter the year you started')
            return
        }

        onAdd({degreeCode, year})
    }



    // Render this if a degree is not loaded
    const startUp = <form className='add-form' onSubmit = {onSubmit}>
        <div className='form-control'>
            <label> Degree Code </label>
            <input className='submit-box-text' 
                type='text' 
                placeholder='Add Degree Code' 
                value={degreeCode} 
                onChange={(e) => setDegreeCode(e.target.value)}
                
            />
        </div>
        <div className='form-control'>
            <label> Implemenetation Year</label>
            <input className='submit-box-text' 
                type='text' 
                placeholder='Add Degree Code'
                value={year} 
                onChange={(e) => setYear(e.target.value)}    
            />
        </div>
        <input className='btn btn-block' type='submit' value='Load Degree'
            onSubmit = {onSubmit}
        />

    </form>

    // Render this if a degree is loaded
    const loadedDegree = 
        <div className='degree'>
            <h2 >
                {degreeCode} - {year}
                <FaTimes 
                    style = { {color:'black', cursor: 'pointer'}} 
                    onClick = {() => onClear()}     
                />
            </h2>
        </div>
        

    function isDegreeLoaded(){
        fetch('/is_degree_loaded').then(response =>
            response.json().then(data => {
                setDegreeLoaded(data.degreeLoaded)
            })
        );

    }

    function displayForm() {
        isDegreeLoaded()
        if (degreeLoaded) {
            fetch('/get_degree').then(response => 
                response.json().then(data => {
                    setDegreeCode(data.degreeCode)
                    setYear(data.year)
                })
            );
            return loadedDegree
        } else {
            return startUp
        }
    }
    /*
    useEffect(() => {
        isDegreeLoaded()
        if (degreeLoaded) {
            fetch('/get_degree').then(response => 
                response.json().then(data => {
                    setDegreeCode(data.degreeCode)
                    setYear(data.year)
                })
            );               
            return loadedDegree
        } else {
            return startUp
        }
    }, [])
    */

    return (
        displayForm()
    )
    
}

export default AddDegree
