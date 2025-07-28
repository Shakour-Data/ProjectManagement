import React, { useEffect, useState } from 'react';
import { ViewMode, Gantt, Task } from 'gantt-task-react';
import 'gantt-task-react/dist/index.css';
import axios from 'axios';

function GanttChart() {
  const [tasks, setTasks] = useState([]);
  const [view, setView] = useState(ViewMode.Day);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchGanttData() {
      try {
        const response = await axios.get('/api/v1/gantt_chart_data');
        const data = response.data;
        // Transform data to gantt-task-react format with custom colors and styles
        const transformedTasks = data.map(task => {
          const progress = Math.min(Math.max(task.progress, 0), 100);
          const isDelayed = new Date(task.end_date) < new Date() && progress < 100;
          return {
            start: new Date(task.start_date),
            end: new Date(task.end_date),
            name: task.name,
            id: task.id,
            type: 'task',
            progress: progress,
            dependencies: task.dependencies,
            styles: {
              progressColor: isDelayed ? '#ff4d4f' : '#1890ff',
              progressSelectedColor: isDelayed ? '#ff7875' : '#40a9ff',
              backgroundColor: '#e6f7ff',
              backgroundSelectedColor: '#bae7ff',
              fontWeight: 'bold',
              fontSize: '14px',
              borderRadius: '4px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            },
            // Tooltip with task info
            render: (task) => (
              <div title={`Task: ${task.name}\nProgress: ${task.progress}%\nStart: ${task.start.toLocaleDateString()}\nEnd: ${task.end.toLocaleDateString()}`}>
                {task.name}
              </div>
            ),
          };
        });
        setTasks(transformedTasks);
        setLoading(false);
      } catch (err) {
        setError('Failed to load Gantt chart data.');
        setLoading(false);
      }
    }
    fetchGanttData();
  }, []);

  if (loading) return <div>Loading Gantt chart...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px', backgroundColor: '#f0f2f5', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <h2 style={{ color: '#1890ff', marginBottom: '15px' }}>Project Gantt Chart</h2>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => setView(ViewMode.Day)} style={{ marginRight: '10px', padding: '6px 12px', borderRadius: '4px', border: 'none', backgroundColor: view === ViewMode.Day ? '#1890ff' : '#f0f0f0', color: view === ViewMode.Day ? '#fff' : '#000', cursor: 'pointer' }}>Day</button>
        <button onClick={() => setView(ViewMode.Week)} style={{ marginRight: '10px', padding: '6px 12px', borderRadius: '4px', border: 'none', backgroundColor: view === ViewMode.Week ? '#1890ff' : '#f0f0f0', color: view === ViewMode.Week ? '#fff' : '#000', cursor: 'pointer' }}>Week</button>
        <button onClick={() => setView(ViewMode.Month)} style={{ padding: '6px 12px', borderRadius: '4px', border: 'none', backgroundColor: view === ViewMode.Month ? '#1890ff' : '#f0f0f0', color: view === ViewMode.Month ? '#fff' : '#000', cursor: 'pointer' }}>Month</button>
      </div>
      <Gantt tasks={tasks} viewMode={view} />
    </div>
  );
}

export default GanttChart;
