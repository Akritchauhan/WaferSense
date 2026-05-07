import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

NUM_WAFERS = 5500
NUM_TELEMETRY = 25000
NUM_MACHINES = 5
NUM_BATCHES = 50

MACHINE_IDS = [f"MACH_{i:03d}" for i in range(1, NUM_MACHINES + 1)]
BATCH_IDS = [f"BATCH_{i:03d}" for i in range(1, NUM_BATCHES + 1)]
ENGINEERS = ["Sarah Chen", "Marcus Rodriguez", "Kenji Tanaka", "Elena Rossi", "David Smith"]
DEFECT_TYPES = ["Micro-crack", "Contamination", "Etch Pit", "Photoresist Residue", "Pattern Distortion"]

def generate_datasets():
    print("Generating Semiconductor Manufacturing Datasets...")
    os.makedirs('datasets', exist_ok=True)

    # ── 1. MAINTENANCE ─────────────────────────────────────────────────────────
    maintenance_rows = []
    for mid in MACHINE_IDS:
        maintenance_rows.append({
            "Machine_ID":        mid,
            "Last_Service_Date": (datetime.now() - timedelta(days=int(np.random.randint(10, 60)))).strftime('%Y-%m-%d'),
            "Downtime_Hours":    round(float(np.random.uniform(2, 12)), 2),
            "Failure_Type":      np.random.choice(
                ["Calibration Drift", "Vacuum Leak", "RF Generator Fault", "Robot Arm Misalignment", "None"],
                p=[0.2, 0.1, 0.1, 0.1, 0.5]
            ),
            "Maintenance_Cost":  round(float(np.random.uniform(500, 5000)), 2),
            "Engineer_Name":     np.random.choice(ENGINEERS),
        })
    df_maintenance = pd.DataFrame(maintenance_rows)

    # ── 2. WAFER MANUFACTURING TABLE ───────────────────────────────────────────
    # Build timestamps in reverse chronological order (most recent first)
    base_time = datetime(2024, 1, 1, 6, 0, 0)
    timestamps = [base_time + timedelta(minutes=15 * i) for i in range(NUM_WAFERS)]

    wafer_rows = []
    for i in range(NUM_WAFERS):
        mid = np.random.choice(MACHINE_IDS)
        bid = np.random.choice(BATCH_IDS)

        # Base process parameters (realistic 90 nm fab values)
        temp     = float(np.random.normal(250, 5))
        pressure = float(np.random.normal(50, 2))
        voltage  = float(np.random.normal(120, 1))
        gas_flow = float(np.random.normal(450, 10))
        etch_t   = float(np.random.uniform(115, 125))

        # ── Inject anomalies for MACH_002 (pressure drift) ──────────────────
        if mid == "MACH_002":
            pressure += float(np.random.normal(4, 1.5))   # consistent high-pressure bias

        # ── Gate Oxide Thickness: 90 nm target, driven by pressure + temp ────
        thickness = 90.0 + (pressure - 50) * 0.4 + (temp - 250) * 0.05 + float(np.random.normal(0, 0.3))

        # ── Defect Count: higher for out-of-spec machines ────────────────────
        base_defects = int(np.random.poisson(2))
        extra = int(abs(thickness - 90) * 1.5)
        defect_count = min(base_defects + extra, 20)

        # ── Yield: realistically spans ~72 % – 99 % ──────────────────────────
        yield_pct = round(max(72.0, min(99.0, 99.0 - defect_count * 1.8 + float(np.random.normal(0, 0.5)))), 2)

        # ── Defect type: only label when defects are meaningful ───────────────
        defect_type = np.random.choice(DEFECT_TYPES) if defect_count >= 4 else "None"

        wafer_rows.append({
            "Wafer_ID":             f"WF_{i+1:06d}",
            "Batch_ID":             bid,
            "Machine_ID":           mid,
            "Process_Step":         "Post-Etch",
            "Yield_Percentage":     yield_pct,
            "Defect_Count":         defect_count,
            "Defect_Type":          defect_type,
            "Gate_Oxide_Thickness": round(thickness, 3),
            "Etch_Time":            round(etch_t, 2),
            "Temperature":          round(temp, 2),
            "Chamber_Pressure":     round(pressure, 2),
            "Voltage":              round(voltage, 2),
            "Gas_Flow_Rate":        round(gas_flow, 2),
            "Timestamp":            timestamps[i].strftime('%Y-%m-%d %H:%M:%S'),
        })
    df_wafers = pd.DataFrame(wafer_rows)

    # ── 3. SENSOR TELEMETRY TABLE ──────────────────────────────────────────────
    tele_rows = []
    tele_base = datetime(2024, 1, 1, 6, 0, 0)
    for i in range(NUM_TELEMETRY):
        mid    = np.random.choice(MACHINE_IDS)
        status = np.random.choice(["Active", "Warning", "Fault"], p=[0.88, 0.09, 0.03])
        drift  = "Stable" if status == "Active" else "Drifting"

        tele_rows.append({
            "Sensor_ID":        f"SENS_{i+1:06d}",
            "Machine_ID":       mid,
            "Pressure_Reading": round(float(np.random.normal(50, 0.8)), 3),
            "Voltage_Reading":  round(float(np.random.normal(120, 0.5)), 3),
            "Gas_Flow":         round(float(np.random.normal(450, 3)), 2),
            "RF_Power":         round(float(np.random.normal(1500, 50)), 1),
            "Temperature":      round(float(np.random.normal(250, 1)), 2),
            "Sensor_Status":    status,
            "Drift_Status":     drift,
            "Timestamp":        (tele_base + timedelta(minutes=3 * i)).strftime('%Y-%m-%d %H:%M:%S'),
        })
    df_telemetry = pd.DataFrame(tele_rows)

    # ── Save ───────────────────────────────────────────────────────────────────
    df_wafers.to_csv('datasets/wafers.csv', index=False)
    df_telemetry.to_csv('datasets/telemetry.csv', index=False)
    df_maintenance.to_csv('datasets/maintenance.csv', index=False)

    # ── Quick validation ───────────────────────────────────────────────────────
    print(f"  Wafer records    : {len(df_wafers):,}")
    print(f"  Telemetry records: {len(df_telemetry):,}")
    print(f"  Maintenance rows : {len(df_maintenance):,}")
    print(f"  Yield range      : {df_wafers.Yield_Percentage.min():.1f}% – {df_wafers.Yield_Percentage.max():.1f}%")
    print(f"  Defect range     : {df_wafers.Defect_Count.min()} – {df_wafers.Defect_Count.max()}")
    print(f"  Pressure range   : {df_wafers.Chamber_Pressure.min():.2f} – {df_wafers.Chamber_Pressure.max():.2f}")
    print(f"  Defect_Type nulls: {df_wafers.Defect_Type.isnull().sum()} (should be 0)")

if __name__ == "__main__":
    generate_datasets()
