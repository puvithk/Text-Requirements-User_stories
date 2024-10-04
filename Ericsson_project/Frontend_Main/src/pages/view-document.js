import React, { useEffect, useState } from 'react';
import "./view-document.css";
import PopUp from './popUp';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { InfinitySpin } from 'react-loader-spinner';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Arrow from './Arrow';
const ViewDoc = () => {
    const navigate = useNavigate();
    const [documentStatus, setDocumentStatus] = useState({
        Requirements: false,
        UserStories: false,
        SRS: false,
        HLD: false,
        LLD: false,
        FullCode: false,
        TOLs : false,
        TestCase : false,
        TestAuto:false
    });
    const [LoadVisible, setLoadVisible] = useState(false);
    const [Loading, setLoading] = useState(false);

    const downloadDocument = async (fileName) => {
        setLoading(true);
        try {
            const link = document.createElement('a');
            link.href = fileName;
            link.download = fileName;
            document.body.appendChild(link);
            toast.success("Document Downloaded")
            setLoading(false);
            link.click();
            document.body.removeChild(link);
        } catch {
            console.log("Error");
            setLoading(false);
        }
    };

    useEffect(() => {
        let previousStatus = documentStatus; // Store previous status

        const interval = setInterval(() => {
            axios.get('http://127.0.0.1:5000/Document_Status')
                .then(response => {
                    const newStatus = response.data;

                    // Detecting changes and triggering actions
                    if (!previousStatus.Requirements && newStatus.Requirements) {
                        toast.success("Requirements document is ready for download!");
                        toast.info("User Stories document is Processing ")
                    }
                    if (!previousStatus.UserStories && newStatus.UserStories) {
                        toast.success("User Stories document is ready for download!");
                        toast.info("SRS document is Processing ")
                    }
                    if (!previousStatus.SRS && newStatus.SRS) {
                        toast.success("SRS document is ready for download!");
                        toast.info("HLD document is Processing ")
                    }
                    if (!previousStatus.HLD && newStatus.HLD) {
                        toast.success("HLD document is ready for download!");
                        toast.info("LLD document is Processing ")
                    }
                    if (!previousStatus.LLD && newStatus.LLD) {
                        toast.success("LLD document is ready for download!");
                        toast.info("TOLs document is Processing ")
                    }
                    if (!previousStatus.FullCode && newStatus.FullCode) {
                        toast.success("Full Code is ready for download!");

                    }
                    if (!previousStatus.TOLs && newStatus.TOLs) {
                        toast.success("TOL  is ready for download!");
                        toast.info("TestCase document is Processing ")
                    }
                    if (!previousStatus.TestCase && newStatus.TestCase) {
                        toast.success("TestCase is ready for download!");
                        toast.info("Test Automation Code is Processing ")
                    }
                    if (!previousStatus.TestAuto && newStatus.TestAuto) {
                        toast.success("Test Automation code is ready for download!");
                        toast.info("Code  is Processing ")
                    }
                    // Update document status with the new state
                    setDocumentStatus(newStatus);
                    previousStatus = newStatus; // Update previousStatus for next check
                })
                .catch(error => console.error("Error fetching document status:", error));
        }, 5000);

        return () => clearInterval(interval); // Clear interval on component unmount
    }, [documentStatus]);

    return (
        <div className='main-download'>
            <ToastContainer className="toaster" />
            {
                Loading ?
                    <div className='main-loading'>
                        <InfinitySpin
                            height="200"
                            width="200"
                            radius="15"
                            color="#3a1c71"
                            ariaLabel="loading"
                        ></InfinitySpin>
                        <div>Creating the Required Document</div>
                    </div>
                    :
                    <div>
                        
                        <div className="download-section">
                        <PopUp setLoadVisible={setLoadVisible} />
                            <button className='Main-button' onClick={() => downloadDocument('http://127.0.0.1:5000/get_all_documents')} disabled={!documentStatus.TestCase}>DOWNLOAD NOW</button>
                        </div>
                       <div className="documents">
    <div className="document-container">
        <div className="document" aria-label="Download Requirements Document">
            Requirements
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_requirements')} disabled={!documentStatus.Requirements} className='ALL-button'>{documentStatus.Requirements ? "DOWNLOAD" : "Processing"}</button>
        </div>
        <Arrow/>
    </div>

    <div className="document-container">
        <div className="document" aria-label="Download User Story Document">
            USER STORY
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_user_stories')} disabled={!documentStatus.UserStories} className='ALL-button'>{documentStatus.UserStories ? "DOWNLOAD" : documentStatus.Requirements ? "Processing": "DOWNLOAD"}</button>
        </div>
        <Arrow/>
    </div>

    <div className="document-container">
        <div className="document" aria-label="Download SRS Document">
            SRS
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_srs')} disabled={!documentStatus.SRS} className='ALL-button'>{documentStatus.SRS ? "DOWNLOAD" : documentStatus.UserStories ? "Processing": "DOWNLOAD"}</button>
        </div>
        <Arrow/>
    </div>

    <div className="document-container">
        <div  className="document" aria-label="Download HLD Document">
            HLD
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_hld')} disabled={!documentStatus.HLD} className='ALL-button'>{documentStatus.HLD ? "DOWNLOAD" : documentStatus.SRS ? "Processing": "DOWNLOAD"}</button>
        </div>
        <Arrow/>
    </div>

    <div className="document-container">
        <div className="document" aria-label="Download LLD Document">
            LLD
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_lld')} disabled={!documentStatus.LLD} className='ALL-button'>{documentStatus.LLD ? "DOWNLOAD" :documentStatus.HLD ? "Processing": "DOWNLOAD"}</button>
        </div>
        <Arrow/>
    </div>

    
    <div className="document-container">
        <div className="document" aria-label="Download Full Code Document">
            TOLs
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_TOL')} disabled={!documentStatus.TOLs} className='ALL-button'>{documentStatus.TOLs ? "DOWNLOAD" : documentStatus.LLD? "Processing": "DOWNLOAD"}</button>
        </div>
        <Arrow/>
    </div>
    <div className="document-container">
        <div className="document" aria-label="Download Full Code Document">
            Test Case 
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_testCase')} disabled={!documentStatus.TestCase} className='ALL-button'>{documentStatus.TestCase ? "DOWNLOAD" : documentStatus.TOLs? "Processing": "DOWNLOAD"}</button>
        </div>
     <Arrow/>
    </div>

    <div className="document-container">
        <div className="document" aria-label="Download Full Code Document">
           Test Automation
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_test_auto')} disabled={!documentStatus.FullCode} className='ALL-button'>{documentStatus.FullCode ? "DOWNLOAD" : documentStatus.LLD? "Processing": "DOWNLOAD"}</button>
        </div>
        <Arrow/>
    </div>


    <div className="document-container">
        <div className="document" aria-label="Download Full Code Document">
            Code
            <button onClick={() => downloadDocument('http://127.0.0.1:5000/get_full_code')} disabled={!documentStatus.FullCode} className='ALL-button'>{documentStatus.FullCode ? "DOWNLOAD" : documentStatus.LLD? "Processing": "DOWNLOAD"}</button>
        </div>
       
    </div>
</div>

                    </div>
            }
        </div>
    );
};

export default ViewDoc;
