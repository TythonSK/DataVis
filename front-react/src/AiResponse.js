import React from 'react';

const AiResponse = ({ response, loading }) => (
  <div className="ai-response">
    {loading ? (
      <div className="spinner">Loading...</div>
    ) : response ? (
      <div className="card">
        <h3>AI Response</h3>
        <p>{response || 'No response from AI.'}</p>
      </div>
    ) : (
      <p>Awaiting AI response...</p>
    )}
  </div>
);

export default AiResponse;
