import React from 'react';

const DataDisplay = ({ text, response, loading }) => (
  <div className="card">
    {loading ? (
      <div className="spinner">Loading...</div>
    ) : response ? (
      <div>
        <h3>AI Response</h3>
        <p>{response}</p>
      </div>
    ) : (
      <p>{text || 'No data available. Please provide input or wait for a response.'}</p>
    )}
  </div>
);

export default DataDisplay;
