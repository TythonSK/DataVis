import React from 'react';

const QueryInput = ({ query, setQuery, handleQuerySubmit }) => (
  <div className="query-container">
    <input
      type="text"
      className="query-input"
      placeholder="Write your query here..."
      value={query}
      onChange={(e) => setQuery(e.target.value)}
    />
    <button onClick={handleQuerySubmit} className="query-submit">Submit</button>
  </div>
);

export default QueryInput;
