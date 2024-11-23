import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ChartDisplay = ({ data }) => {
  const chartData = {
    labels: ['January', 'February', 'March', 'April', 'May'],  // Example labels
    datasets: [
      {
        label: 'Sample Data',
        data: data.chartData || [12, 19, 3, 5, 2],  // Example data
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <div className="card ChartDisplay">
      {/* The responsive option ensures the chart adjusts automatically */}
      <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
    </div>
  );
};

export default ChartDisplay;
