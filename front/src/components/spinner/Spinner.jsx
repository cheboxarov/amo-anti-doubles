import React from 'react';
import './Spinner.css';
import { HashLoader } from 'react-spinners'

const Spinner = () => {
    return (
        <div className="spinner">
            <HashLoader />
        </div>
    );
};

export default Spinner;
