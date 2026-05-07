-- SEMICONDUCTOR FABRICATION ANALYSIS - SQL QUERIES

-- 1. Joining Wafer Data with Machine Maintenance Info
SELECT 
    w.Wafer_ID, 
    w.Machine_ID, 
    m.Engineer_Name,
    w.Yield_Percentage
FROM wafers w
INNER JOIN maintenance m ON w.Machine_ID = m.Machine_ID
LIMIT 10;

-- 2. Ranking Machines by Highest Defect Counts
SELECT 
    Machine_ID, 
    SUM(Defect_Count) AS Total_Defects,
    ROUND(AVG(Yield_Percentage), 2) AS Avg_Yield
FROM wafers
GROUP BY Machine_ID
ORDER BY Total_Defects DESC;

-- 3. Calculating Average Yield per Batch
SELECT 
    Batch_ID, 
    ROUND(AVG(Yield_Percentage), 2) AS Batch_Yield
FROM wafers
GROUP BY Batch_ID
HAVING Batch_Yield < 90
ORDER BY Batch_Yield ASC;

-- 4. Identifying Abnormal Pressure Readings (Outlier Detection)
SELECT 
    Wafer_ID, 
    Machine_ID, 
    Chamber_Pressure
FROM wafers
WHERE Chamber_Pressure > 55 OR Chamber_Pressure < 45
ORDER BY Chamber_Pressure DESC;

-- 5. Defect Percentage Calculation using CASE Statement
SELECT 
    Machine_ID,
    COUNT(Wafer_ID) AS Total_Wafers,
    SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END) AS Failed_Wafers,
    ROUND(CAST(SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(Wafer_ID) * 100, 2) AS Failure_Rate_Pct
FROM wafers
GROUP BY Machine_ID;

-- 6. Analyzing Correlation between Pressure and Defects (Simple CTE)
WITH HighPressureWafers AS (
    SELECT Wafer_ID, Machine_ID, Defect_Count, Chamber_Pressure
    FROM wafers
    WHERE Chamber_Pressure > 52
)
SELECT 
    Machine_ID, 
    AVG(Defect_Count) as Avg_Defects_At_High_Pressure
FROM HighPressureWafers
GROUP BY Machine_ID;
