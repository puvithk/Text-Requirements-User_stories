import React, { useState } from 'react';
import './PopUp.css'; // Import the CSS file for styling

const ToolKit = (props) => {
   
  return (

        <div className="popup-box">
          <div className="popup-pointer"></div> {/* Triangle pointer */}
          <div className="popup-content">
            <div className="popup-icon">
              <i className="fas fa-volume-up"></i> {/* Example Icon */}
            </div>
            <div className="popup-message">
              <p>The Document is Processing..........</p>
           
            </div>
          </div>
        </div>
      
    
  );
};

export default ToolKit;
