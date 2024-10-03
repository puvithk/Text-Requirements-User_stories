import React, { useState, useRef, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Corrected navigator issue
import {Audio,InfinitySpin } from 'react-loader-spinner'
const FrontPage = () => {
  const [uploadStatus, setUploadStatus] = useState({ show: false, success: false, message: '' });
  const [selectedFile, setSelectedFile] = useState(null); // Store the selected file
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // Corrected the navigator issue
  useEffect(()=>{
    try{
      const response = axios.get("http://localhost:5000/refresh")
      .then((response) => {
        console.log(response.data);
    })}
      catch{
        console.log('Error')
      }
    }
  ,[])
  const onDrop = (acceptedFiles) => {
    // Store the selected file from the dropzone
    const file = acceptedFiles[0];
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus({ show: true, success: false, message: 'No file selected' });
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 1800000,
      });

      // Assuming the API returns some data and no errors
      setUploadStatus({ show: true, success: true, message: 'Upload successful!' });
      navigate('/download'); // Navigate to the download page after successful upload
    } catch (error) {
      setUploadStatus({ show: true, success: false, message: `Upload failed: ${error.message}` });
    } finally {
      setLoading(false);
    }

    // Hide the status after 5 seconds
    setTimeout(() => {
      setUploadStatus((prevStatus) => ({ ...prevStatus, show: false }));
    }, 5000);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: '.txt',
    maxSize: 5 * 1024 * 1024, // 5MB
  });

  return (
    <div className="background">
      {loading ? (
        <div className='main-loading'>
          <InfinitySpin
          height="200"
          width="200"
          radius="15"
          color="#3a1c71"
          ariaLabel="loading"
          ></InfinitySpin>
          <div>loading....</div>
        </div>
      ) : (
        <>
          <div className="floating-shape shape1"></div>
          <div className="floating-shape shape2"></div>
          <div className="floating-shape shape3"></div>
          <div className="container">
            <h1>Upload The Requirements</h1>
            <p className="subtitle">Upload your text documents</p>

            <div {...getRootProps()} className="dropzone">
              <input {...getInputProps()} />
              {isDragActive ? (
                <p>Drop the files here ...</p>
              ) : (
                <p>Drop your text file here or click to select</p>
              )}
            </div>

            {/* Display selected file name inside a text input box */}
            {selectedFile && (
              <input
                type="text"
                className="file-input"
                value={selectedFile.name}
                readOnly
                style={{ marginTop: '10px', padding: '5px', width: '100%' }}
              />
            )}

            <button onClick={handleUpload} className="upload-button" style={{ marginTop: '15px' }}>
              Upload File
            </button>

            {uploadStatus.show && (
              <div className={`upload-status ${uploadStatus.success ? 'success' : 'error'}`}>
                <i className={`fas ${uploadStatus.success ? 'fa-check-circle' : 'fa-times-circle'}`}></i>
                <span>{uploadStatus.message}</span>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default FrontPage;
