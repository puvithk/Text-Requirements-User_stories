import React from 'react'

import "./view-document.css"

import PopUp from './popUp';

import { useState } from "react"
import { useNavigate } from 'react-router-dom';
const  downloadDocument=(fileName) =>{
    
    const link = document.createElement('a');
    link.href = fileName;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
};


const ViewDoc=()=>{
    const navigate = useNavigate()
    const [LoadVisible , setLoadVisible ] = useState(false)
    


    return (
        <div className='main-download'>
        <PopUp setLoadVisible={setLoadVisible}/>
        <div className="download-section">
        <button onClick={()=>downloadDocument('http://127.0.0.1:5000/get_all_documents')}>DOWNLOAD NOW</button>
        </div>
        <div className="documents">
        <div 
        className="document"
        onClick={()=>downloadDocument('http://127.0.0.1:5000/get_requirements')} aria-label="Download User Story Document">
     Requirements
        </div>
        <div 
        className="document"
        onClick={()=>downloadDocument('http://127.0.0.1:5000/get_user_stories')} aria-label="Download User Story Document">
     
            USER STORY
        </div>

        <div className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_srs')}aria-label="Download SRS Document">
            <i className="fas fa-file-pdf"></i>
            SRS
        </div>

        <div 
        className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_hld')}aria-label="Download HLD Document">
            <i className="fas fa-file-pdf"></i>
            HLD
        </div>
        <div 
        className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_lld')} aria-label="Download LLD Document">
            <i className="fas fa-file-pdf"></i>
            LLD
        </div>
        <div className='code-download'>

        <div 
        className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_full_code')} aria-label="Download LLD Document">
            <i className="fas fa-file-pdf"></i>
            Code 
        </div>
        </div>

    </div>
    </div>
    );
};



export default ViewDoc;

    

    
     
        
   
    
