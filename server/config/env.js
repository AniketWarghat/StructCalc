// server/config/env.js
require('dotenv').config();

module.exports = {
    PORT: process.env.PORT || 5000,
    // The local address pointing to where your Python FastAPI service runs
    PYTHON_ENGINE_URL: process.env.PYTHON_ENGINE_URL || 'http://127.0.0.1:8000'
};