import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function App() {
  const [progressReport, setProgressReport] = useState(null);
  const [priorityReport, setPriorityReport] = useState(null);
  const [costReport, setCostReport] = useState(null);
  const [resourceReport, setResourceReport] = useState(null);
  const [riskReport, setRiskReport] = useState(null);

  useEffect(() => {
    axios.get('/api/progress_report')
      .then(response => setProgressReport(response.data))
      .catch(error => console.error('Error fetching progress report:', error));

    axios.get('/api/priority_urgency_report')
      .then(response => setPriorityReport(response.data))
      .catch(error => console.error('Error fetching priority report:', error));

    axios.get('/api/cost_management_report')
      .then(response => setCostReport(response.data))
      .catch(error => console.error('Error fetching cost report:', error));

    axios.get('/api/resource_allocation_report')
      .then(response => setResourceReport(response.data))
      .catch(error => console.error('Error fetching resource report:', error));

    axios.get('/api/risk_management_report')
      .then(response => setRiskReport(response.data))
      .catch(error => console.error('Error fetching risk report:', error));
  }, []);

  return (
    <div className="container py-4">
      <h1 className="mb-4">Project Management Dashboard</h1>

      <section className="mb-5">
        <h2 className="mb-3">Progress Report</h2>
        {progressReport ? (
          <div className="card p-3 shadow-sm">
            <p>Total Tasks: <strong>{progressReport.total_tasks}</strong></p>
            <p>Completed Tasks: <strong>{progressReport.completed_tasks}</strong></p>
            <p>In Progress Tasks: <strong>{progressReport.in_progress_tasks}</strong></p>
            <p>Pending Tasks: <strong>{progressReport.pending_tasks}</strong></p>
          </div>
        ) : (
          <p>Loading progress report...</p>
        )}
      </section>

      <section className="mb-5">
        <h2 className="mb-3">Priority and Urgency Report</h2>
        {priorityReport ? (
          <BarChart width={600} height={300} data={priorityReport['Important & Urgent']}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="importance" fill="#0d6efd" />
            <Bar dataKey="urgency" fill="#198754" />
          </BarChart>
        ) : (
          <p>Loading priority report...</p>
        )}
      </section>

      <section className="mb-5">
        <h2 className="mb-3">Cost Management Report</h2>
        {costReport ? (
          <pre className="bg-light p-3 rounded">{JSON.stringify(costReport, null, 2)}</pre>
        ) : (
          <p>Loading cost report...</p>
        )}
      </section>

      <section className="mb-5">
        <h2 className="mb-3">Resource Allocation Report</h2>
        {resourceReport ? (
          <pre className="bg-light p-3 rounded">{JSON.stringify(resourceReport, null, 2)}</pre>
        ) : (
          <p>Loading resource report...</p>
        )}
      </section>

      <section className="mb-5">
        <h2 className="mb-3">Risk Management Report</h2>
        {riskReport ? (
          <pre className="bg-light p-3 rounded">{JSON.stringify(riskReport, null, 2)}</pre>
        ) : (
          <p>Loading risk report...</p>
        )}
      </section>
    </div>
  );
}

export default App;
