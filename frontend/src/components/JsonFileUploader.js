import React, { useState, useEffect } from 'react';
import axios from 'axios';

const JsonFileUploader = ({ onComplete, projectId }) => {
  const [files, setFiles] = useState([]);
  const [currentFileIndex, setCurrentFileIndex] = useState(0);
  const [status, setStatus] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch list of JSON files inside wbs_parts folder from backend
    const fetchFiles = async () => {
      try {
        const response = await axios.get('/api/user_inputs/list_wbs_parts', { params: { project_id: projectId } });
        setFiles(response.data.files);
      } catch (err) {
        setError('Failed to load WBS parts file list');
      }
    };
    fetchFiles();
  }, [projectId]);

  const uploadFile = async (fileName) => {
    setStatus(`Uploading ${fileName}...`);
    setError(null);
    try {
      // Fetch file content from user input or local file system
      // For demo, we simulate file content
      const fileContent = '{}'; // Replace with actual file content
      await axios.post(`/api/user_inputs/upload/${fileName}`, fileContent, {
        headers: { 'Content-Type': 'application/json' },
        params: { project_id: projectId },
      });
      setStatus(`${fileName} uploaded successfully.`);
      if (currentFileIndex + 1 < files.length) {
        setCurrentFileIndex(currentFileIndex + 1);
      } else {
        // After all uploads, trigger aggregation
        await axios.post('/api/user_inputs/aggregate_wbs', null, { params: { project_id: projectId } });
        onComplete();
      }
    } catch (err) {
      setError(`Failed to upload ${fileName}: ${err.message}`);
    }
  };

  useEffect(() => {
    if (files.length > 0 && currentFileIndex < files.length) {
      uploadFile(files[currentFileIndex]);
    }
  }, [currentFileIndex, files]);

  return (
    <div>
      <h2>JSON File Upload Wizard</h2>
      {error ? (
        <div style={{ color: 'red' }}>
          <p>{error}</p>
          <button onClick={() => uploadFile(files[currentFileIndex])}>Retry</button>
        </div>
      ) : (
        <p>{status}</p>
      )}
      <p>
        Uploading file {currentFileIndex + 1} of {files.length}
      </p>
    </div>
  );
};

export default JsonFileUploader;
