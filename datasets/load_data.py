import sqlite3
import pandas as pd
import os

def load_data():
    db_path = 'wafersense.db'
    
    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read schema
    with open('sql/schema.sql', 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    print("Schema created. Loading datasets...")
    
    # Load Wafers
    df_wafers = pd.read_csv('datasets/wafers.csv')
    df_wafers.to_sql('wafers', conn, if_exists='replace', index=False)
    print(f"Loaded {len(df_wafers)} records into 'wafers' table.")
    
    # Load Telemetry
    df_telemetry = pd.read_csv('datasets/telemetry.csv')
    df_telemetry.to_sql('telemetry', conn, if_exists='replace', index=False)
    print(f"Loaded {len(df_telemetry)} records into 'telemetry' table.")
    
    # Load Maintenance
    df_maintenance = pd.read_csv('datasets/maintenance.csv')
    df_maintenance.to_sql('maintenance', conn, if_exists='replace', index=False)
    print(f"Loaded {len(df_maintenance)} records into 'maintenance' table.")
    
    conn.commit()
    conn.close()
    print("Database indexing complete. Ready for analysis.")

if __name__ == "__main__":
    load_data()
