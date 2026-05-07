import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import warnings
import os

warnings.filterwarnings('ignore')

# Professional corporate theme
plt.rcParams.update({
    'figure.facecolor': '#F8F9FA',
    'axes.facecolor':   '#FFFFFF',
    'axes.edgecolor':   '#CCCCCC',
    'axes.grid':        True,
    'grid.color':       '#EEEEEE',
    'font.family':      'DejaVu Sans',
    'font.size':        11,
    'axes.titlesize':   14,
    'axes.titleweight': 'bold',
    'axes.labelsize':   11,
})
PALETTE = 'Blues_d'

os.makedirs('screenshots', exist_ok=True)


def run_analytics():
    print("Running Python Analytics Pipeline...")

    conn = sqlite3.connect('wafersense.db')
    df   = pd.read_sql_query("SELECT * FROM wafers", conn)
    df_t = pd.read_sql_query("SELECT * FROM telemetry", conn)
    conn.close()

    print(f"  Loaded: {len(df):,} wafer records, {len(df_t):,} telemetry records")

    # ── 1. Data Cleaning: remove nulls, duplicates ───────────────────────────
    df = df.drop_duplicates()
    df['Defect_Type'].fillna('None', inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # ── 2. Outlier Removal: IQR on Gate Oxide Thickness ─────────────────────
    Q1, Q3 = df['Gate_Oxide_Thickness'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    df_clean = df[
        (df['Gate_Oxide_Thickness'] >= Q1 - 1.5 * IQR) &
        (df['Gate_Oxide_Thickness'] <= Q3 + 1.5 * IQR)
    ]
    print(f"  IQR outliers removed: {len(df) - len(df_clean)}")

    # ── 3. Correlation Heatmap ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 8))
    cols = ['Yield_Percentage', 'Defect_Count', 'Gate_Oxide_Thickness',
            'Chamber_Pressure', 'Voltage', 'Gas_Flow_Rate', 'Temperature']
    corr = df_clean[cols].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
                linewidths=0.5, ax=ax, square=True)
    ax.set_title('Process Parameter Correlation Heatmap')
    fig.tight_layout()
    fig.savefig('screenshots/correlation_heatmap.png', dpi=200)
    plt.close(fig)

    # ── 4. Yield Distribution by Machine (Box Plot) ──────────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df_clean, x='Machine_ID', y='Yield_Percentage',
                hue='Machine_ID', palette='Blues', legend=False, ax=ax)
    ax.set_title('Yield Distribution by Machine ID')
    ax.set_xlabel('Machine ID')
    ax.set_ylabel('Yield (%)')
    ax.axhline(90, color='red', linestyle='--', linewidth=1.2, label='90% Threshold')
    ax.legend()
    fig.tight_layout()
    fig.savefig('screenshots/yield_by_machine.png', dpi=200)
    plt.close(fig)

    # ── 5. Chamber Pressure Distribution (Box Plot) ──────────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df_clean, x='Machine_ID', y='Chamber_Pressure',
                hue='Machine_ID', palette='Oranges', legend=False, ax=ax)
    ax.set_title('Chamber Pressure Distribution — MACH_002 Shows Drift')
    ax.set_xlabel('Machine ID')
    ax.set_ylabel('Chamber Pressure (mTorr)')
    ax.axhline(52, color='red', linestyle='--', linewidth=1.2, label='Upper Control Limit (52)')
    ax.axhline(48, color='orange', linestyle='--', linewidth=1.2, label='Lower Control Limit (48)')
    ax.legend()
    fig.tight_layout()
    fig.savefig('screenshots/pressure_distribution.png', dpi=200)
    plt.close(fig)

    # ── 6. Gate Oxide Thickness vs Chamber Pressure (Scatter) ────────────────
    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(
        df_clean['Chamber_Pressure'], df_clean['Gate_Oxide_Thickness'],
        c=df_clean['Yield_Percentage'], cmap='RdYlGn',
        alpha=0.5, s=20, edgecolors='none'
    )
    plt.colorbar(sc, ax=ax, label='Yield (%)')
    ax.set_title('Chamber Pressure vs Gate Oxide Thickness\n(Color = Yield %)')
    ax.set_xlabel('Chamber Pressure (mTorr)')
    ax.set_ylabel('Gate Oxide Thickness (nm)')
    ax.axhline(90, color='blue', linestyle='--', linewidth=1, label='90 nm Target')
    ax.legend()
    fig.tight_layout()
    fig.savefig('screenshots/thickness_vs_pressure.png', dpi=200)
    plt.close(fig)

    # ── 7. Defect Type Distribution ──────────────────────────────────────────
    df_defects = df_clean[df_clean['Defect_Type'] != 'None']
    fig, ax = plt.subplots(figsize=(10, 6))
    order = df_defects['Defect_Type'].value_counts().index
    sns.countplot(data=df_defects, x='Defect_Type', hue='Defect_Type',
                  order=order, palette='viridis', legend=False, ax=ax)
    ax.set_title('Distribution of Post-Etch Defect Types')
    ax.set_xlabel('Defect Type')
    ax.set_ylabel('Count')
    plt.xticks(rotation=20)
    fig.tight_layout()
    fig.savefig('screenshots/defect_distribution.png', dpi=200)
    plt.close(fig)

    # ── 8. Yield Trend over Time ─────────────────────────────────────────────
    df_trend = df_clean.set_index('Timestamp').resample('7D')['Yield_Percentage'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df_trend['Timestamp'], df_trend['Yield_Percentage'],
            color='steelblue', linewidth=2, marker='o', markersize=4)
    ax.fill_between(df_trend['Timestamp'], df_trend['Yield_Percentage'],
                    alpha=0.15, color='steelblue')
    ax.axhline(90, color='red', linestyle='--', linewidth=1.2, label='90% Threshold')
    ax.set_title('Weekly Average Yield Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Avg Yield (%)')
    ax.legend()
    fig.tight_layout()
    fig.savefig('screenshots/yield_trends.png', dpi=200)
    plt.close(fig)

    print("  All visualizations saved to /screenshots")

    # ── 9. Statistical Summary ───────────────────────────────────────────────
    print("\n  === Statistical Insights ===")
    corr_val = df_clean[['Chamber_Pressure', 'Gate_Oxide_Thickness']].corr().iloc[0, 1]
    print(f"  Pressure <-> Thickness correlation : {corr_val:.3f}")
    low_yield = df_clean[df_clean['Yield_Percentage'] < 85]
    print(f"  Wafers with Yield < 85%          : {len(low_yield)} ({len(low_yield)/len(df_clean)*100:.1f}%)")
    print(f"  Machine with most defects        : {df_clean.groupby('Machine_ID')['Defect_Count'].sum().idxmax()}")


if __name__ == "__main__":
    run_analytics()
