import React from 'react';
import { parseCSVData } from './CSVToDataParser'; // Import the CSV parser function
import html2canvas from 'html2canvas';

const DatasetSelector = ({ dataset, setDataset, model, setModel, setCsvChartData, chartRef }) => {
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const csvData = e.target.result;
        const { labels, values } = parseCSVData(csvData); // Parse the CSV file
        setCsvChartData({
          chartData: values,
          labels,
        });
      };
      reader.readAsText(file);
    }
  };

  // Function to download the chart as PNG
  const handleDownloadClick = () => {
    if (chartRef.current) {
      html2canvas(chartRef.current).then((canvas) => {
        // Convert canvas to a PNG and download it
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = 'chart.png';
        link.click();
      });
    }
  };

  return (
    <div className="controls">
      <select
        className="dataset-select"
        value={dataset || ""}
        onChange={(e) => setDataset(e.target.value)}
      >
        <option value="">Choose dataset</option>
        <option value="dataset1">Dataset 1</option>
        <option value="dataset2">Dataset 2</option>
      </select>

      <select
        className="model-select"
        value={model || ""}
        onChange={(e) => setModel(e.target.value)}
      >
        <option value="">Predictive model</option>
        <option value="model1">Model 1</option>
        <option value="model2">Model 2</option>
      </select>

      {/* File upload for CSV */}
      <input type="file" className="upload-dataset" accept=".csv" onChange={handleFileUpload} />

      {/* Download PNG Button */}
      <button onClick={handleDownloadClick} className="download-btn">
        Download Chart as PNG
      </button>
    </div>
  );
};

export default DatasetSelector;
