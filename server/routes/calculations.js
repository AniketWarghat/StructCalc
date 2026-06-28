// server/routes/calculations.js
const express = require("express");
const router = express.Router(); // Fixed capitalization
const { PYTHON_ENGINE_URL } = require("../config/env");

router.post("/beam", async (req, res, next) => {
    try {
        const beamInputs = req.body;

        // Fixed single quotes to backticks
        console.log(`[Express Proxy]: Forwarding inputs to python engine at ${PYTHON_ENGINE_URL}/calc/beam`);

        // Fixed single quotes to backticks
        const engineResponse = await fetch(`${PYTHON_ENGINE_URL}/calc/beam`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(beamInputs)
        });

        // ADD THESE TWO LINES: Extract the data and return it to the user!
        const calculations = await engineResponse.json();
        return res.status(engineResponse.status).json(calculations);

    } catch (error) {
        console.error("[Express Proxy Error]: Python Calculation Engine is unreachable.");
        next(error);
    }
});

module.exports = router;