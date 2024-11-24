import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatasetSelector from './DatasetSelector';
import QueryInput from './QueryInput';
import ChartDisplay from './ChartDisplay';
import DataDisplay from './DataDisplay';
import './App.css';
import './DatasetSelector.css';
import './QueryInput.css';
import './ChartDisplay.css';
import './DataDisplay.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [model, setModel] = useState('');
  const [csvChartData, setCsvChartData] = useState(null);

  useEffect(() => {
    if (dataset && model) {
      setLoading(true);
      axios
        .get(`http://localhost:5000/api/data?dataset=${dataset}&model=${model}`)
        .then((response) => {
          setData(response.data);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        })
        .finally(() => {
          setLoading(false);
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
          setCsvChartData={setCsvChartData} // Pass down state setter
        />

        <div className="data-container">
          <div className="card DataDisplay">
            <DataDisplay text={data?.text || null} response={response} loading={loading} />
          </div>

          <div className="card ChartDisplay">
            {csvChartData ? (
              <ChartDisplay data={csvChartData} />
            ) : (
              <ChartDisplay data={data || {}} />
            )}
          </div>
        </div>

        <div className="query-container-bottom">
          <QueryInput
            query={query}
            setQuery={setQuery}
            handleQuerySubmit={async () => {
              if (!query) return;

              setLoading(true);
              try {
                const aiResponse = await axios.post('http://localhost:5000/api/ai', { query });
                setResponse(aiResponse.data.response);
              } catch (error) {
                console.error('Error processing query:', error);
                setResponse('An error occurred while fetching AI response.');
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
