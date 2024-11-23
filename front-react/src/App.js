// src/App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState(null);  // State to store the fetched data

  // useEffect to run once when the component mounts
  useEffect(() => {
    axios.get('http://localhost:5000/api/data')  // Replace with your backend endpoint
      .then(response => {
        setData(response.data);  // Save the fetched data into the state
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);  // Empty array ensures this effect runs only once when the component mounts

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data from Python Backend</h1>
        {data ? (
          <pre>{JSON.stringify(data, null, 2)}</pre>  // Format the response data
        ) : (
          <p>Loading...</p>
        )}
      </header>
    </div>
  );
}

export default App;
