import React from 'react';

const Arrow = () => {
    return (
        <svg width="80" height="60" xmlns="http://www.w3.org/2000/svg" className="arrow-svg">
            {/* Increased strokeWidth to 20 and adjusted line's y1 and y2 to center it */}
            <line x1="0" y1="30" x2="50" y2="30" stroke="green" strokeWidth="20" />
            {/* Adjusted the polygon points to fit the new width */}
            <polygon points="50,15 80,30 50,45" fill="green" />
        </svg>
    );
};

export default Arrow;
