import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ChartDisplay = ({ data }) => {
  // Default fallback chart data
  const fallbackData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], // Default labels
    datasets: [
      {
        label: 'No data available',
        data: [0, 0, 0, 0, 0], // Empty chart
        backgroundColor: 'rgba(200, 200, 200, 0.5)',
        borderColor: 'rgba(200, 200, 200, 0.8)',
      },
    ],
  };

  const chartData = data?.chartData
    ? {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], // Your actual labels
        datasets: [
          {
            label: 'Sample Data',
            data: data.chartData,
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 0.8)',
          },
        ],
      }
    : fallbackData;

  return (
    <div className="card ChartDisplay">
      <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
    </div>
  );
};

export default ChartDisplay;
