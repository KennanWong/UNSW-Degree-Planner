import React from 'react'

const Button = ({onClick}) => {
    
    return (
        <button onClick = {onClick} className='btn'>
            Submit
        </button>
    )
}

export default Button
