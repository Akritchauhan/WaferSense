-- ============================================================
--  WaferSense - Database Schema
--  Semiconductor Fabrication Yield & Sensor Optimization
-- ============================================================

-- Table 1: Wafer Manufacturing Table
CREATE TABLE IF NOT EXISTS wafers (
    Wafer_ID              TEXT PRIMARY KEY,
    Batch_ID              TEXT    NOT NULL,
    Machine_ID            TEXT    NOT NULL,
    Process_Step          TEXT    DEFAULT 'Post-Etch',
    Yield_Percentage      REAL    CHECK(Yield_Percentage BETWEEN 0 AND 100),
    Defect_Count          INTEGER CHECK(Defect_Count >= 0),
    Defect_Type           TEXT    DEFAULT 'None',
    Gate_Oxide_Thickness  REAL,
    Etch_Time             REAL,
    Temperature           REAL,
    Chamber_Pressure      REAL,
    Voltage               REAL,
    Gas_Flow_Rate         REAL,
    Timestamp             DATETIME
);

-- Table 2: Sensor Telemetry Table
CREATE TABLE IF NOT EXISTS telemetry (
    Sensor_ID        TEXT PRIMARY KEY,
    Machine_ID       TEXT NOT NULL,
    Pressure_Reading REAL,
    Voltage_Reading  REAL,
    Gas_Flow         REAL,
    RF_Power         REAL,
    Temperature      REAL,
    Sensor_Status    TEXT DEFAULT 'Active',
    Drift_Status     TEXT DEFAULT 'Stable',
    Timestamp        DATETIME
);

-- Table 3: Machine Maintenance Table
CREATE TABLE IF NOT EXISTS maintenance (
    Machine_ID         TEXT PRIMARY KEY,
    Last_Service_Date  DATE,
    Downtime_Hours     REAL,
    Failure_Type       TEXT DEFAULT 'None',
    Maintenance_Cost   REAL,
    Engineer_Name      TEXT
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_wafers_machine   ON wafers(Machine_ID);
CREATE INDEX IF NOT EXISTS idx_wafers_batch     ON wafers(Batch_ID);
CREATE INDEX IF NOT EXISTS idx_wafers_timestamp ON wafers(Timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_machine ON telemetry(Machine_ID);

-- Executive Summary View
CREATE VIEW IF NOT EXISTS v_executive_summary AS
SELECT
    Machine_ID,
    COUNT(Wafer_ID)                                                        AS Total_Wafers,
    ROUND(AVG(Yield_Percentage), 2)                                        AS Avg_Yield,
    SUM(Defect_Count)                                                      AS Total_Defects,
    SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END)                AS Failed_Wafers,
    ROUND(CAST(SUM(CASE WHEN Yield_Percentage < 90 THEN 1 ELSE 0 END)
          AS FLOAT) / COUNT(Wafer_ID) * 100, 2)                           AS Failure_Rate_Pct
FROM wafers
GROUP BY Machine_ID;
