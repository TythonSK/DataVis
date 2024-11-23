import React from 'react';

const DatasetSelector = ({ dataset, setDataset, model, setModel }) => (
  <div className="controls">
    <select
      className="dataset-select"
      value={dataset}
      onChange={(e) => setDataset(e.target.value)}
    >
      <option value="">Choose dataset</option>
      <option value="dataset1">Dataset 1</option>
      <option value="dataset2">Dataset 2</option>
    </select>
    <select
      className="model-select"
      value={model}
      onChange={(e) => setModel(e.target.value)}
    >
      <option value="">Predictive model</option>
      <option value="model1">Model 1</option>
      <option value="model2">Model 2</option>
    </select>
    <input type="file" className="upload-dataset" />
  </div>
);

export default DatasetSelector;
