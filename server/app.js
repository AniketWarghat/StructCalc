// server/app.js
const express = require('express');
const cors = require('cors');
const calculationRoutes = require('./routes/calculations'); // Import your new router file
require('dotenv').config();

const app = express();

app.use(cors());
app.use(express.json());

// Mount the router under the base API path layout prefix
app.use('/api/calc', calculationRoutes); // This builds the final working URL: /api/calc/beam

app.get('/api/health', (req, res) => {
    res.status(200).json({ 
        status: "active", 
        gateway: "structacalc-api-server" 
    });
});

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: "Internal Server Routing Exception",
        message: err.message 
    });
});

module.exports = app;