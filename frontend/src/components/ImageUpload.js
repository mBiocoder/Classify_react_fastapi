import React, { useState } from "react";

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [classification, setClassification] = useState("");
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setClassification(""); // Clear any previous classification
    setError(null); // Clear any previous error
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:8000/classify/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setClassification(data.classification);
      } else {
        setError("Classification failed. Please try again.");
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      setError("An error occurred. Please try again later.");
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h2>Image Classifier</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Classify</button>
      {error && <p>Error: {error}</p>}
      {classification && <p>Classification: {classification}</p>}
    </div>
  );
};

export default ImageUpload;
