import Papa from 'papaparse';

export const parseCSVData = (csvString) => {
  const result = Papa.parse(csvString, { header: true });
  const data = result.data;

  // Extract labels (dates) and values for a specific country
  const country = 'Zimbabwe' // HARD-CODED - TODO: UN-HARD-CODE IT
  const labels = [];
  const values = [];

  data.forEach((row) => {
    if (row['Country/Region'] === country) {
      Object.keys(row).forEach((key) => {
        if (key.match(/^\d{1,2}\/\d{1,2}\/\d{2}$/)) { // Match date columns like "1/22/20"
          labels.push(key);
          values.push(parseInt(row[key], 10) || 0); // Default to 0 if NaN
        }
      });
    }
  });

  return { labels, values };
};
