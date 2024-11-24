import React from 'react';
import { parseCSVData } from './CSVToDataParser'; // Import the CSV parser function
import html2canvas from 'html2canvas';

const DatasetSelector = ({ setCsvChartData, chartRef }) => {
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

  const handleDownloadClick = () => {
    if (chartRef.current) {
      html2canvas(chartRef.current).then((canvas) => {
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = 'chart.png';
        link.click();
      });
    }
  };

  return (
    <div className="controls">
      {/* File upload button with styled label */}
      <label htmlFor="upload-dataset" className="upload-btn">
        Vybrať Súbor
      </label>
      <input
        id="upload-dataset"
        type="file"
        className="upload-dataset"
        accept=".csv"
        onChange={handleFileUpload}
      />

      {/* Download PNG Button */}
      <button onClick={handleDownloadClick} className="download-btn">
        Download Chart as PNG
      </button>
    </div>
  );
};

export default DatasetSelector;
