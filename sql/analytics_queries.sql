-- 1. Machine-wise Yield and Defect Analysis
-- Calculates total defects and average yield for each machine
SELECT 
    Machine_ID,
    COUNT(Wafer_ID) AS Total_Wafers,
    ROUND(AVG(Yield_Percentage), 2) AS Avg_Yield,
    SUM(Defect_Count) AS Total_Defects,
    ROUND(AVG(Chamber_Pressure), 2) AS Avg_Pressure
FROM wafers
GROUP BY Machine_ID
ORDER BY Avg_Yield ASC;

-- 2. Identifying Machines with Highest Defects using CTE
WITH MachineDefects AS (
    SELECT 
        Machine_ID,
        SUM(Defect_Count) as Total_Defects,
        RANK() OVER (ORDER BY SUM(Defect_Count) DESC) as Defect_Rank
    FROM wafers
    GROUP BY Machine_ID
)
SELECT * FROM MachineDefects WHERE Defect_Rank <= 3;

-- 3. Pressure Drift Analysis using Window Functions
-- Detects if the current pressure is significantly different from the machine's moving average
SELECT 
    Wafer_ID,
    Machine_ID,
    Chamber_Pressure,
    AVG(Chamber_Pressure) OVER (PARTITION BY Machine_ID ORDER BY Timestamp ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) as Moving_Avg_Pressure,
    (Chamber_Pressure - AVG(Chamber_Pressure) OVER (PARTITION BY Machine_ID ORDER BY Timestamp ROWS BETWEEN 5 PRECEDING AND CURRENT ROW)) as Deviation
FROM wafers
LIMIT 20;

-- 4. Batch-wise Yield Performance with CASE statement
SELECT 
    Batch_ID,
    AVG(Yield_Percentage) as Avg_Yield,
    CASE 
        WHEN AVG(Yield_Percentage) >= 95 THEN 'Excellent'
        WHEN AVG(Yield_Percentage) >= 90 THEN 'Good'
        WHEN AVG(Yield_Percentage) >= 85 THEN 'Needs Attention'
        ELSE 'Critical'
    END AS Yield_Status
FROM wafers
GROUP BY Batch_ID
HAVING Avg_Yield < 95
ORDER BY Avg_Yield ASC;

-- 5. Sensor Instability Analysis
-- Linking Wafer failures with sensor drift status
SELECT 
    w.Wafer_ID,
    w.Machine_ID,
    w.Yield_Percentage,
    t.Drift_Status,
    t.Sensor_Status
FROM wafers w
INNER JOIN telemetry t ON w.Machine_ID = t.Machine_ID AND ABS(JULIANDAY(w.Timestamp) - JULIANDAY(t.Timestamp)) * 1440 < 5
WHERE w.Yield_Percentage < 90
LIMIT 50;

-- 6. VIEW: Executive Yield Summary
CREATE VIEW IF NOT EXISTS v_executive_summary AS
SELECT 
    Machine_ID,
    COUNT(Wafer_ID) as Total_Production,
    ROUND(AVG(Yield_Percentage), 2) as Yield_Score,
    SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END) as Failed_Wafers
FROM wafers
GROUP BY Machine_ID;

-- 7. Yield Degradation Trend
SELECT 
    STRFTIME('%Y-%m-%d', Timestamp) as Date,
    AVG(Yield_Percentage) as Daily_Yield
FROM wafers
GROUP BY Date
ORDER BY Date DESC;
