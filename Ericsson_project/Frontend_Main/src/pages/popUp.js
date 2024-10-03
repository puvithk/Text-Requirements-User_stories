import React, { useState } from 'react';
import './PopUp.css'; // Import the CSS file for styling
import image from "./close.png"
import axios from 'axios';

import { useNavigate } from 'react-router-dom';
const PopUp = (props) => {
    const navigate = useNavigate()
  const [isVisible, setIsVisible] = useState(false);
  const handelClick =async ()=>{
    props.setLoadVisible(true)
    try{
   const response = await axios.get('http://localhost:5000/refresh')
   .then(()=>{
     props.setLoadVisible(false)
  navigate("/") 
   })
     
   
}     catch{
    console.log("Error")
}
    }

        
  const showPopUp = () => {
    setIsVisible(true);
  };

  const hidePopUp = () => {
    setIsVisible(false);
  };

  return (
    <div className="popup-container">
      <button
        style={{width : "10px"}} 
        className="popup-button" 
        onMouseEnter={showPopUp} 
        onMouseLeave={hidePopUp}
        onClick={handelClick}
      >
        <img src={image}></img>
      </button>

      {isVisible && (
        <div className="popup-box">
          <div className="popup-pointer"></div> {/* Triangle pointer */}
          <div className="popup-content">
            <div className="popup-icon">
              <i className="fas fa-volume-up"></i> {/* Example Icon */}
            </div>
            <div className="popup-message">
              <p>Close, Will delete all the File</p>
           
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PopUp;
