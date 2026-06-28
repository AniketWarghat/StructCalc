// server/server.js
const app = require('./app');

// Look at your system environment variables for a port, or fall back to local 5000
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`==================================================`);
    console.log(` StructCalc API GATEWAY RUNNING ON PORT: ${PORT}`);
    console.log(`==================================================`);
});