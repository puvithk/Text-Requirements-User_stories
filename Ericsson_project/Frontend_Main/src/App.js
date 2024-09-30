import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import "./App.css"
import FrontPage from "../src/pages/FrontPage"
import ViewDoc from '../src/pages/view-document';
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FrontPage />} />
        <Route path="/download" element={<ViewDoc />} />
      </Routes>
    </Router>
  );
};

export default App;
