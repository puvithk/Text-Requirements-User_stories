import React from 'react'

import "./view-document.css"

import PopUp from './popUp';
import axios from 'axios';
import { useState } from "react"
import { useNavigate } from 'react-router-dom';

import { Audio,InfinitySpin } from 'react-loader-spinner';

const ViewDoc=()=>{
    const navigate = useNavigate()
    const [LoadVisible , setLoadVisible ] = useState(false)
    
    const [Loading ,setLoading] = useState(false)
    const  downloadDocument=async (fileName) =>{
        setLoading(true)
        try{
            const response = axios.get(fileName)
                .then(()=>{
                const link = document.createElement('a');
                link.href = fileName;
                link.download = fileName;
                document.body.appendChild(link);
                setLoading(false)
                link.click();
                document.body.removeChild(link);
                })
        }
        catch{
            console.log("Error")
            setLoading(false)
        }
        
    };
    
    return (
        <div className='main-download'>
            {
               Loading?
                <div className='main-loading'>
          <InfinitySpin
          height="200"
          width="200"
          radius="15"
          color="#3a1c71"
          ariaLabel="loading"
          wrapperStyle
          wrapperClass
          ></InfinitySpin>
          <div>Creating the Required Document</div>
        </div>
                :
                <div>
        <PopUp setLoadVisible={setLoadVisible}/>
        <div className="download-section">
        <button className='Main-button' onClick={()=>downloadDocument('http://127.0.0.1:5000/get_all_documents')}>DOWNLOAD NOW</button>
        </div>
        <div className="documents">
        <div 
        className="document"
        onClick={()=>downloadDocument('http://127.0.0.1:5000/get_requirements')} aria-label="Download User Story Document">
     Requirements
        
        <button className='ALL-button'>DOWNLOAD</button>
        </div><div 
        className="document"
        onClick={()=>downloadDocument('http://127.0.0.1:5000/get_user_stories')} aria-label="Download User Story Document">
     
            USER STORY
            <button className='ALL-button'>DOWNLOAD</button>
        </div>

        <div className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_srs')}aria-label="Download SRS Document">
            <i className="fas fa-file-pdf"></i>
            SRS
            <button className='ALL-button'>DOWNLOAD</button>
        </div>

        <div 
        className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_hld')}aria-label="Download HLD Document">
            <i className="fas fa-file-pdf"></i>
            HLD
            <button className='ALL-button'>DOWNLOAD</button>
        </div>
        <div 
        className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_lld')} aria-label="Download LLD Document">
            <i className="fas fa-file-pdf"></i>
            LLD
            <button className='ALL-button'>DOWNLOAD</button>
        </div>
        <div className='code-download'>

        <div 
        className="document"
         onClick={()=>downloadDocument('http://127.0.0.1:5000/get_full_code')} aria-label="Download LLD Document">
            <i className="fas fa-file-pdf"></i>
            Code 
            <button className='ALL-button'>DOWNLOAD</button>
        </div>
        </div>

    </div>
    </div>
      }
    </div>
    );
};



export default ViewDoc;

    

    
     
        
   
    
