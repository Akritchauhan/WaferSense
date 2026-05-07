import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)

# Configuration
NUM_WAFERS = 10500
NUM_TELEMETRY = 52000
NUM_MACHINES = 5
NUM_BATCHES = 100

def generate_datasets():
    print("Generating Semiconductor Manufacturing Datasets...")
    
    # 1. Machines and Maintenance
    machine_ids = [f"MACH_{i:03d}" for i in range(1, NUM_MACHINES + 1)]
    engineers = ["Sarah Chen", "Marcus Rodriguez", "Kenji Tanaka", "Elena Rossi", "David Smith"]
    
    maintenance_data = []
    for m_id in machine_ids:
        maintenance_data.append({
            "Machine_ID": m_id,
            "Last_Service_Date": (datetime.now() - timedelta(days=np.random.randint(10, 60))).strftime('%Y-%m-%d'),
            "Downtime_Hours": np.random.uniform(2, 12),
            "Failure_Type": np.random.choice(["Calibration Drift", "Vacuum Leak", "RF Generator Fault", "Robot Arm Misalignment", "None"], p=[0.2, 0.1, 0.1, 0.1, 0.5]),
            "Maintenance_Cost": np.random.uniform(500, 5000),
            "Engineer_Name": np.random.choice(engineers)
        })
    df_maintenance = pd.DataFrame(maintenance_data)
    
    # 2. Wafer Manufacturing Table
    batch_ids = [f"BATCH_{i:03d}" for i in range(1, NUM_BATCHES + 1)]
    
    wafer_ids = [f"WF_{i:06d}" for i in range(1, NUM_WAFERS + 1)]
    timestamps = [datetime.now() - timedelta(minutes=i*15) for i in range(NUM_WAFERS)]
    
    wafers = []
    for i in range(NUM_WAFERS):
        m_id = np.random.choice(machine_ids)
        b_id = np.random.choice(batch_ids)
        
        # Base process parameters
        temp = np.random.normal(250, 5)
        pressure = np.random.normal(50, 2)
        voltage = np.random.normal(120, 1)
        gas_flow = np.random.normal(450, 10)
        
        # Inject Anomaly: MACH_002 has Chamber Pressure Drift
        if m_id == "MACH_002":
            pressure += np.random.normal(5, 1) # Higher pressure drift
            
        # Gate Oxide Thickness depends on Pressure and Temperature
        # Ideal: 90nm. Deviation based on pressure.
        thickness = 90 + (pressure - 50) * 0.5 + np.random.normal(0, 0.2)
        
        # Yield and Defects
        defect_count = int(max(0, np.random.poisson(2) + (abs(thickness - 90) * 2)))
        yield_pct = max(0, min(100, 98 - (defect_count * 0.5)))
        
        defect_types = ["Micro-crack", "Contamination", "Etch Pit", "Photoresist Residue", "Pattern Distortion"]
        d_type = np.random.choice(defect_types) if defect_count > 5 else "None"
        
        wafers.append({
            "Wafer_ID": wafer_ids[i],
            "Batch_ID": b_id,
            "Machine_ID": m_id,
            "Process_Step": "Post-Etch",
            "Yield_Percentage": round(yield_pct, 2),
            "Defect_Count": defect_count,
            "Defect_Type": d_type,
            "Gate_Oxide_Thickness": round(thickness, 3),
            "Etch_Time": round(np.random.uniform(115, 125), 2),
            "Temperature": round(temp, 2),
            "Chamber_Pressure": round(pressure, 2),
            "Voltage": round(voltage, 2),
            "Gas_Flow_Rate": round(gas_flow, 2),
            "Timestamp": timestamps[i].strftime('%Y-%m-%d %H:%M:%S')
        })
    df_wafers = pd.DataFrame(wafers)
    
    # 3. Sensor Telemetry Table
    telemetry = []
    for i in range(NUM_TELEMETRY):
        m_id = np.random.choice(machine_ids)
        # Random status and drift
        status = np.random.choice(["Active", "Warning", "Fault"], p=[0.9, 0.08, 0.02])
        drift = "Stable" if status == "Active" else "Drifting"
        
        telemetry.append({
            "Sensor_ID": f"SENS_{i:06d}",
            "Machine_ID": m_id,
            "Voltage_Reading": round(np.random.normal(120, 0.5), 3),
            "Pressure_Reading": round(np.random.normal(50, 0.1), 3),
            "Gas_Flow": round(np.random.normal(450, 2), 2),
            "RF_Power": round(np.random.normal(1500, 50), 1),
            "Temperature": round(np.random.normal(250, 1), 2),
            "Sensor_Status": status,
            "Drift_Status": drift,
            "Timestamp": (datetime.now() - timedelta(minutes=i*3)).strftime('%Y-%m-%d %H:%M:%S')
        })
    df_telemetry = pd.DataFrame(telemetry)
    
    # Save to CSV
    os.makedirs('datasets', exist_ok=True)
    df_wafers.to_csv('datasets/wafers.csv', index=False)
    df_telemetry.to_csv('datasets/telemetry.csv', index=False)
    df_maintenance.to_csv('datasets/maintenance.csv', index=False)
    
    print(f"Successfully generated:")
    print(f" - {len(df_wafers)} Wafer records")
    print(f" - {len(df_telemetry)} Telemetry records")
    print(f" - {len(df_maintenance)} Maintenance records")

if __name__ == "__main__":
    generate_datasets()
