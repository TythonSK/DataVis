import React from 'react';

const AiResponse = ({ response, loading }) => (
  <div className="ai-response">
    {loading ? (
      <div className="spinner">Loading...</div>
    ) : response ? (
      <div className="card">
        <h3>AI Response</h3>
        <p>{response.result || 'No result from AI.'}</p>
      </div>
    ) : (
      <p>Failed to load AI response.</p>
    )}
  </div>
);

export default AiResponse;
