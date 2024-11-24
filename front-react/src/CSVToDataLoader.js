import React, { useState } from 'react';
import ChartDisplay from './ChartDisplay'; // Your chart component
import { parseCSVData } from './utils'; // The CSV parsing function

const App = () => {
  const [chartData, setChartData] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const csvData = e.target.result;
        const { labels, values } = parseCSVData(csvData);

        setChartData({
          chartData: values,
          labels,
        });
      };

      reader.readAsText(file);
    }
  };

  return (
    <div>
      <h1>CSV to Chart</h1>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      {chartData && <ChartDisplay data={chartData} />}
    </div>
  );
};

export default App;
