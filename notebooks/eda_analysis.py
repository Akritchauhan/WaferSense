import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Set professional style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

def run_analytics():
    print("Running Python Analytics Pipeline...")
    conn = sqlite3.connect('wafersense.db')
    df = pd.read_sql_query("SELECT * FROM wafers", conn)
    
    os.makedirs('screenshots', exist_ok=True)
    
    # 1. Data Cleaning: Outlier Removal (IQR Method)
    Q1 = df['Gate_Oxide_Thickness'].quantile(0.25)
    Q3 = df['Gate_Oxide_Thickness'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_clean = df[(df['Gate_Oxide_Thickness'] >= lower_bound) & (df['Gate_Oxide_Thickness'] <= upper_bound)]
    print(f"Removed {len(df) - len(df_clean)} outliers using IQR method.")

    # 2. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    corr = df[['Yield_Percentage', 'Defect_Count', 'Gate_Oxide_Thickness', 'Chamber_Pressure', 'Voltage', 'Gas_Flow_Rate', 'Temperature']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Process Parameter Correlation Heatmap', fontsize=16)
    plt.savefig('screenshots/correlation_heatmap.png', dpi=300)
    plt.close()

    # 3. Yield Trend Analysis by Machine
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df, x='Timestamp', y='Yield_Percentage', hue='Machine_ID', alpha=0.6)
    plt.title('Yield Percentage Trends Over Time by Machine', fontsize=16)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('screenshots/yield_trends.png', dpi=300)
    plt.close()

    # 4. Chamber Pressure Analysis (Box Plot)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Machine_ID', y='Chamber_Pressure', hue='Machine_ID', palette='magma', legend=False)
    plt.title('Chamber Pressure Distribution Across Machines', fontsize=16)
    plt.savefig('screenshots/pressure_distribution.png', dpi=300)
    plt.close()

    # 5. Gate Oxide Thickness vs Chamber Pressure (Scatter Plot)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Chamber_Pressure', y='Gate_Oxide_Thickness', hue='Yield_Percentage', size='Defect_Count', sizes=(20, 200), alpha=0.7)
    plt.title('Gate Oxide Thickness vs. Chamber Pressure', fontsize=16)
    plt.savefig('screenshots/thickness_vs_pressure.png', dpi=300)
    plt.close()

    # 6. Defect Type Distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df[df['Defect_Type'] != 'None'], x='Defect_Type', hue='Defect_Type', palette='viridis', legend=False)
    plt.title('Distribution of Defect Types', fontsize=16)
    plt.xticks(rotation=30)
    plt.savefig('screenshots/defect_distribution.png', dpi=300)
    plt.close()

    print("Analytics reports generated in /screenshots directory.")
    conn.close()

if __name__ == "__main__":
    run_analytics()
