import React, { useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import mammoth from "mammoth";

const DatasetSelector = ({ dataset, setDataset, model, setModel }) => {
  const [fileContent, setFileContent] = useState("");

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const fileType = file.type;

    try {
      if (fileType === "application/pdf") {
        // Handle PDF files
        const content = await extractTextFromPDF(file);
        setFileContent(content);
      } else if (
        fileType ===
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
        fileType === "application/msword"
      ) {
        // Handle Word documents
        const content = await extractTextFromWord(file);
        setFileContent(content);
      } else if (fileType.startsWith("text/")) {
        // Handle plain text files
        const content = await file.text();
        setFileContent(content);
      } else {
        setFileContent("Unsupported file type!");
      }
    } catch (error) {
      console.error("Error processing file:", error);
      setFileContent("Error reading file!");
    }
  };

  const extractTextFromPDF = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const pdf = await pdfjsLib.getDocument({ data: e.target.result }).promise;
          let text = "";
          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            text += content.items.map((item) => item.str).join(" ");
          }
          resolve(text);
        } catch (error) {
          reject(error);
        }
      };
      reader.onerror = (e) => reject(e.target.error);
      reader.readAsArrayBuffer(file);
    });
  };

  const extractTextFromWord = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        mammoth
          .extractRawText({ arrayBuffer: e.target.result })
          .then((result) => resolve(result.value))
          .catch((error) => reject(error));
      };
      reader.onerror = (e) => reject(e.target.error);
      reader.readAsArrayBuffer(file);
    });
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

      <input
        type="file"
        className="upload-dataset"
        accept=".txt, .pdf, .doc, .docx"
        onChange={handleFileChange}
      />

      {/* Display extracted file content */}
      {fileContent && <pre className="file-content">{fileContent}</pre>}
    </div>
  );
};

export default DatasetSelector;
