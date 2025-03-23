import React from 'react';

export const RomaniaFlag = ({ sx }) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 30" width="24" height="15" style={sx}>
            <path d="M0 0h16.67v30H0z" fill="#002B7F" />
            <path d="M16.67 0h16.66v30H16.67z" fill="#FCD116" />
            <path d="M33.33 0h16.67v30H33.33z" fill="#D10000" />
        </svg>
    );
}
