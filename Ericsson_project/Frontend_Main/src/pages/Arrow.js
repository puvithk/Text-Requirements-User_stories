import React from 'react';

const Arrow = () => {
    return (
        <svg width="60" height="60" xmlns="http://www.w3.org/2000/svg" className="arrow-svg">
            {/* Adjusted strokeWidth and the line's x2 to match the new width */}
            <line x1="0" y1="30" x2="40" y2="30" stroke="green" strokeWidth="20" />
            {/* Adjusted the polygon points to fit the new width */}
            <polygon points="40,15 60,30 40,45" fill="green" />
        </svg>
    );
};

export default Arrow;
