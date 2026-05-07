import sqlite3
import pandas as pd

conn = sqlite3.connect('wafersense.db')

queries = [
    ("Q1 Machine Yield", "SELECT Machine_ID, ROUND(AVG(Yield_Percentage),2) AS Avg_Yield, SUM(Defect_Count) AS Total_Defects FROM wafers GROUP BY Machine_ID ORDER BY Avg_Yield ASC"),
    ("Q2 CTE Top Defects", "WITH D AS (SELECT Machine_ID, SUM(Defect_Count) as Defects, RANK() OVER (ORDER BY SUM(Defect_Count) DESC) as Rnk FROM wafers GROUP BY Machine_ID) SELECT * FROM D WHERE Rnk<=3"),
    ("Q3 Batch CASE", "SELECT Batch_ID, ROUND(AVG(Yield_Percentage),2) AS Avg_Yield, CASE WHEN AVG(Yield_Percentage)>=95 THEN 'Excellent' WHEN AVG(Yield_Percentage)>=90 THEN 'Good' ELSE 'Needs Attention' END AS Status FROM wafers GROUP BY Batch_ID ORDER BY Avg_Yield ASC LIMIT 5"),
    ("Q4 JOIN+Failed", "SELECT w.Wafer_ID, w.Machine_ID, m.Engineer_Name, w.Yield_Percentage FROM wafers w INNER JOIN maintenance m ON w.Machine_ID=m.Machine_ID WHERE w.Yield_Percentage < 85 LIMIT 5"),
    ("Q5 Pressure Anomaly", "SELECT Wafer_ID, Machine_ID, Chamber_Pressure FROM wafers WHERE Chamber_Pressure > 54 OR Chamber_Pressure < 46 ORDER BY Chamber_Pressure DESC LIMIT 5"),
    ("Q6 Failure Rate", "SELECT Machine_ID, ROUND(CAST(SUM(CASE WHEN Yield_Percentage<90 THEN 1 ELSE 0 END) AS FLOAT)/COUNT(Wafer_ID)*100,2) AS Failure_Rate_Pct FROM wafers GROUP BY Machine_ID ORDER BY Failure_Rate_Pct DESC"),
    ("Q7 High Pressure CTE", "WITH HP AS (SELECT Machine_ID, Defect_Count, Yield_Percentage FROM wafers WHERE Chamber_Pressure > 52) SELECT Machine_ID, ROUND(AVG(Defect_Count),2) AS Avg_Defects FROM HP GROUP BY Machine_ID ORDER BY Avg_Defects DESC"),
    ("Q8 Drift HAVING", "SELECT Machine_ID, ROUND(CAST(SUM(CASE WHEN Drift_Status='Drifting' THEN 1 ELSE 0 END) AS FLOAT)/COUNT(Sensor_ID)*100,2) AS Drift_Pct FROM telemetry GROUP BY Machine_ID ORDER BY Drift_Pct DESC"),
    ("VIEW Executive Summary", "SELECT * FROM v_executive_summary"),
]

all_pass = True
for name, q in queries:
    try:
        df = pd.read_sql_query(q, conn)
        rows = len(df)
        flag = "PASS" if rows > 0 else "WARN-0rows"
        if flag != "PASS":
            all_pass = False
        print(f"[{flag}] {name}: {rows} rows")
        print(df.to_string(index=False))
        print()
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        all_pass = False

print("========================================")
print("Result: ALL PASS" if all_pass else "Result: SOME ISSUES FOUND")
conn.close()
