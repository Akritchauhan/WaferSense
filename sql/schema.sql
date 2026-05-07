-- Table 1: Wafer Manufacturing Table
CREATE TABLE IF NOT EXISTS wafers (
    Wafer_ID TEXT PRIMARY KEY,
    Batch_ID TEXT,
    Machine_ID TEXT,
    Process_Step TEXT,
    Yield_Percentage REAL,
    Defect_Count INTEGER,
    Defect_Type TEXT,
    Gate_Oxide_Thickness REAL,
    Etch_Time REAL,
    Temperature REAL,
    Chamber_Pressure REAL,
    Voltage REAL,
    Gas_Flow_Rate REAL,
    Timestamp DATETIME
);

-- Table 2: Sensor Telemetry Table
CREATE TABLE IF NOT EXISTS telemetry (
    Sensor_ID TEXT PRIMARY KEY,
    Machine_ID TEXT,
    Voltage_Reading REAL,
    Pressure_Reading REAL,
    Gas_Flow REAL,
    RF_Power REAL,
    Temperature REAL,
    Sensor_Status TEXT,
    Drift_Status TEXT,
    Timestamp DATETIME
);

-- Table 3: Machine Maintenance Table
CREATE TABLE IF NOT EXISTS maintenance (
    Machine_ID TEXT PRIMARY KEY,
    Last_Service_Date DATE,
    Downtime_Hours REAL,
    Failure_Type TEXT,
    Maintenance_Cost REAL,
    Engineer_Name TEXT
);

-- Creating Indexes for Optimization
CREATE INDEX IF NOT EXISTS idx_wafers_machine ON wafers(Machine_ID);
CREATE INDEX IF NOT EXISTS idx_wafers_batch ON wafers(Batch_ID);
CREATE INDEX IF NOT EXISTS idx_telemetry_machine ON telemetry(Machine_ID);
