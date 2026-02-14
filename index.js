const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

app.get('/api/info', (req, res) => {
  res.json({
    name: 'Documentation AI Agent',
    version: '1.0.0',
    description: 'API service for documentation AI agent',
    endpoints: ['/api/health', '/api/info', '/api/echo'],
  });
});

app.post('/api/echo', (req, res) => {
  res.json({
    echoed: req.body,
    receivedAt: new Date().toISOString(),
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
