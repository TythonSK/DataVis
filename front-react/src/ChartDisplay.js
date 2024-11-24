import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ChartDisplay = ({ data, chartRef }) => {
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
        labels: data.labels,
        datasets: [
          {
            label: 'Confirmed Cases',
            data: data.chartData,
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 0.8)',
            fill: false,
          },
        ],
      }
    : fallbackData;

  return (
    <div className="chart-canvas" ref={chartRef}> {/* Attach ref here */}
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
