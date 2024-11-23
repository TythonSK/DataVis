import React from 'react';

const DataDisplay = ({ text }) => (
  <div className="card">
    <h3>Text Output</h3>
    <p>{text || 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'}</p>
  </div>
);

export default DataDisplay;
