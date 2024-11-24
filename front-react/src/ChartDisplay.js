import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ChartDisplay = ({ data }) => {
  const fallbackData = {
    labels: ['No Data'], // Default labels
    datasets: [
      {
        label: 'No data available',
        data: [0], // Empty chart
        backgroundColor: 'rgba(200, 200, 200, 0.5)',
        borderColor: 'rgba(200, 200, 200, 0.8)',
      },
    ],
  };

  const chartData = data?.labels && data?.chartData
    ? {
        labels: data.labels, // Pass labels from the parent component
        datasets: [
          {
            label: 'Confirmed Cases',
            data: data.chartData, // Pass dataset values
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 0.8)',
            fill: false,
          },
        ],
      }
    : fallbackData;

  return (
    <div className="card ChartDisplay">
      <Line
        data={chartData}
        options={{
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { title: { display: true, text: 'Dates' } },
            y: { title: { display: true, text: 'Confirmed Cases' } },
          },
        }}
      />
    </div>
  );
};


export default ChartDisplay;
