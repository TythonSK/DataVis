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
    const [loading, setLoading] = useState(false); // State to manage loading state
    const [query, setQuery] = useState(''); // Query input field state
    const [response, setResponse] = useState(null); // AI response state
    const [dataset, setDataset] = useState(null); // Dataset state
    const [model, setModel] = useState(''); // Predictive model state

    // Fetch data from the backend when dataset and model are selected
    useEffect(() => {
      if (dataset && model) {
        setLoading(true); // Start loading
        axios
          .get(`http://localhost:5000/api/data?dataset=${dataset}&model=${model}`)
          .then((response) => {
            setData(response.data); // Set fetched data
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          })
          .finally(() => {
            setLoading(false); // Stop loading
          });
      }
    }, [dataset, model]);

    return (
      <div className="App">
        <header className="App-header">
          <h1>AI-Powered Mockup Design</h1>

          {/* Dataset Selector */}
          <DatasetSelector
            dataset={dataset}
            setDataset={setDataset}
            model={model}
            setModel={setModel}
          />

          {/* AI Response */}
          <AiResponse response={response} loading={loading} />

        {/* Displaying the fetched data */}
        {data && (
          <div className="data-container">
            {/* Text output on the left */}
            <div className="card DataDisplay">
              <DataDisplay text={data.text} />
            </div>

            {/* Visualized data (Chart) on the right */}
            <div className="card ChartDisplay">
              <ChartDisplay data={data} />
              <ChartDisplay data={data} />
              <ChartDisplay data={data} />
            </div>
          </div>
        )}

          {/* Query Input */}
          <div className="query-container-bottom">
            <QueryInput
              query={query}
              setQuery={setQuery}
              handleQuerySubmit={async () => {
                if (!query) return;

                //console.log("Sending query:", query);


                setLoading(true); // Set loading state
                try {
                  const aiResponse = await axios.post('http://localhost:5000/api/ai', { query });
                  setResponse(aiResponse.data.response); // Set AI response
                  console.log("Sending query:", query);
                  

                } catch (error) {
                  console.error('Error processing query:', error);
                  setResponse('An error occurred while fetching AI response.');
                } finally {
                  setLoading(false); // Reset loading state
                }
              }}
            />
          </div>
        </header>
      </div>
    );
  }

  export default App;
