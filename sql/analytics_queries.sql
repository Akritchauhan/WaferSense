-- ============================================================
--  WaferSense - Analytical SQL Queries
--  Semiconductor Fabrication Yield & Sensor Optimization
--  Level: Beginner to Intermediate | Interview-Ready
-- ============================================================


-- ─────────────────────────────────────────────────────────────
-- Q1. Machine-wise Yield & Defect Summary
--     Business Use: Find which machine produces the most defects
-- ─────────────────────────────────────────────────────────────
SELECT
    Machine_ID,
    COUNT(Wafer_ID)                 AS Total_Wafers,
    ROUND(AVG(Yield_Percentage), 2) AS Avg_Yield_Pct,
    SUM(Defect_Count)               AS Total_Defects,
    ROUND(AVG(Chamber_Pressure), 2) AS Avg_Pressure
FROM wafers
GROUP BY Machine_ID
ORDER BY Avg_Yield_Pct ASC;


-- ─────────────────────────────────────────────────────────────
-- Q2. Top 3 Worst Machines by Defect Count (CTE + Window Fn)
--     Business Use: Prioritize maintenance on the highest-risk equipment
-- ─────────────────────────────────────────────────────────────
WITH MachineDefects AS (
    SELECT
        Machine_ID,
        SUM(Defect_Count)                                      AS Total_Defects,
        RANK() OVER (ORDER BY SUM(Defect_Count) DESC)          AS Defect_Rank
    FROM wafers
    GROUP BY Machine_ID
)
SELECT * FROM MachineDefects
WHERE Defect_Rank <= 3;


-- ─────────────────────────────────────────────────────────────
-- Q3. Batch-wise Yield with Performance Rating (CASE Statement)
--     Business Use: Flag poor batches for quality review
-- ─────────────────────────────────────────────────────────────
SELECT
    Batch_ID,
    ROUND(AVG(Yield_Percentage), 2) AS Avg_Yield,
    CASE
        WHEN AVG(Yield_Percentage) >= 95 THEN 'Excellent'
        WHEN AVG(Yield_Percentage) >= 90 THEN 'Good'
        WHEN AVG(Yield_Percentage) >= 85 THEN 'Needs Attention'
        ELSE 'Critical – Investigate'
    END AS Yield_Status
FROM wafers
GROUP BY Batch_ID
ORDER BY Avg_Yield ASC
LIMIT 20;


-- ─────────────────────────────────────────────────────────────
-- Q4. Join Wafer Data with Engineer Information
--     Business Use: Trace each failed wafer back to the responsible engineer
-- ─────────────────────────────────────────────────────────────
SELECT
    w.Wafer_ID,
    w.Machine_ID,
    m.Engineer_Name,
    m.Last_Service_Date,
    w.Yield_Percentage,
    w.Defect_Count
FROM wafers w
INNER JOIN maintenance m ON w.Machine_ID = m.Machine_ID
WHERE w.Yield_Percentage < 85
ORDER BY w.Yield_Percentage ASC
LIMIT 20;


-- ─────────────────────────────────────────────────────────────
-- Q5. Abnormal Chamber Pressure Detection (WHERE + ORDER BY)
--     Business Use: Spot sensor readings outside normal operating range
-- ─────────────────────────────────────────────────────────────
SELECT
    Wafer_ID,
    Machine_ID,
    Chamber_Pressure,
    Yield_Percentage,
    Timestamp
FROM wafers
WHERE Chamber_Pressure > 54 OR Chamber_Pressure < 46
ORDER BY Chamber_Pressure DESC
LIMIT 30;


-- ─────────────────────────────────────────────────────────────
-- Q6. Defect Failure Rate per Machine (CASE inside SUM)
--     Business Use: Calculate % of wafers that fall below quality threshold
-- ─────────────────────────────────────────────────────────────
SELECT
    Machine_ID,
    COUNT(Wafer_ID)                                                          AS Total_Wafers,
    SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END)                  AS Failed_Wafers,
    ROUND(
        CAST(SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END) AS FLOAT)
        / COUNT(Wafer_ID) * 100, 2
    )                                                                        AS Failure_Rate_Pct
FROM wafers
GROUP BY Machine_ID
ORDER BY Failure_Rate_Pct DESC;


-- ─────────────────────────────────────────────────────────────
-- Q7. High-Pressure Wafer Analysis using CTE
--     Business Use: Test hypothesis that high pressure causes more defects
-- ─────────────────────────────────────────────────────────────
WITH HighPressureWafers AS (
    SELECT Wafer_ID, Machine_ID, Defect_Count, Chamber_Pressure, Yield_Percentage
    FROM wafers
    WHERE Chamber_Pressure > 52
)
SELECT
    Machine_ID,
    COUNT(Wafer_ID)                 AS Wafers_At_High_Pressure,
    ROUND(AVG(Defect_Count), 2)     AS Avg_Defects,
    ROUND(AVG(Yield_Percentage), 2) AS Avg_Yield
FROM HighPressureWafers
GROUP BY Machine_ID
ORDER BY Avg_Defects DESC;


-- ─────────────────────────────────────────────────────────────
-- Q8. Sensor Drift Summary (HAVING Filter)
--     Business Use: Find machines with frequent sensor warnings
-- ─────────────────────────────────────────────────────────────
SELECT
    Machine_ID,
    COUNT(Sensor_ID)                                                  AS Total_Readings,
    SUM(CASE WHEN Drift_Status = 'Drifting' THEN 1 ELSE 0 END)       AS Drifting_Count,
    ROUND(
        CAST(SUM(CASE WHEN Drift_Status = 'Drifting' THEN 1 ELSE 0 END) AS FLOAT)
        / COUNT(Sensor_ID) * 100, 2
    )                                                                 AS Drift_Pct
FROM telemetry
GROUP BY Machine_ID
HAVING Drift_Pct > 5
ORDER BY Drift_Pct DESC;
