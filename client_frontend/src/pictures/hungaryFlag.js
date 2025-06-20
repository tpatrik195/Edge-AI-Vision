import React from 'react';

export const HungaryFlag = ({ sx }) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 30" width="24" height="15" style={sx}>
            <path d="M0 0h50v10H0z" fill="#ce2939" />
            <path d="M0 10h50v10H0z" fill="#ffffff" />
            <path d="M0 20h50v10H0z" fill="#477050" />
        </svg>
    );
}
