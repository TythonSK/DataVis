import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatasetSelector from './DatasetSelector';
import QueryInput from './QueryInput';
import AiResponse from './AiResponse';
import ChartDisplay from './ChartDisplay';
import DataDisplay from './DataDisplay';
import './App.css';
import './DatasetSelector.css';
import './QueryInput.css';
import './AiResponse.css';
import './ChartDisplay.css';
import './DataDisplay.css';

function App() {
  const [data, setData] = useState(null); // State to store fetched data
  const [loading, setLoading] = useState(true); // State to manage loading state
  const [query, setQuery] = useState(''); // Query input field state
  const [response, setResponse] = useState(null); // AI response state
  const [dataset, setDataset] = useState(null); // Dataset state
  const [model, setModel] = useState(''); // Predictive model state

  // Fetch data from the backend when the component mounts
  useEffect(() => {
    if (dataset && model) {
      axios
        .get(`http://localhost:5000/api/data?dataset=${dataset}&model=${model}`)
        .then((response) => {
          setData(response.data); // Set the data to the state
          setLoading(false); // Set loading to false once data is fetched
        })
        .catch((error) => {
          console.error('There was an error fetching the data!', error);
          setLoading(false); // Set loading to false if there's an error
        });
    }
  }, [dataset, model]); // Runs when dataset or model changes

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered Mockup Design</h1>

        {/* Dataset Selector Component */}
        <DatasetSelector
          dataset={dataset}
          setDataset={setDataset}
          model={model}
          setModel={setModel}
        />

        {/* AI Response Component */}
        <AiResponse response={response} loading={loading} />

        {/* Displaying the fetched data */}
        {data && (
          <div className="data-container">
            {/* Text output on the left */}
            <div className="card DataDisplay">
              <h3>Text Output</h3>
              <DataDisplay text={data.text} />
            </div>

            {/* Visualized data (Chart) on the right */}
            <div className="card ChartDisplay">
              <h3>Visualized Data</h3>
              <ChartDisplay data={data} />
            </div>
          </div>
        )}

        {/* Query Input (at the bottom) */}
        <div className="query-container-bottom">
          <QueryInput
            query={query}
            setQuery={setQuery}
            handleQuerySubmit={async () => {
              if (!query) return;

              setLoading(true);
              try {
                const aiResponse = await axios.post('http://localhost:5000/api/ai', { query });
                setResponse(aiResponse.data);
              } catch (error) {
                console.error('Error processing query:', error);
              } finally {
                setLoading(false);
              }
            }}
          />
        </div>
      </header>
    </div>
  );
}

export default App;
