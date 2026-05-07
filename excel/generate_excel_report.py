import pandas as pd
import numpy as np
import xlsxwriter
import sqlite3
import os

def generate_cost_of_quality_report():
    print("Generating Cost of Quality Analysis Excel Workbook...")
    
    # 1. Fetch Data
    conn = sqlite3.connect('wafersense.db')
    df = pd.read_sql_query("SELECT * FROM wafers", conn)
    
    # 2. Define Financial Constants
    COST_PER_WAFER = 500  # Manufacturing cost per wafer
    SCRAP_VAL = 50        # Recovery value of scrapped wafer
    REWORK_COST = 120     # Cost to rework a minor defect
    TOTAL_PROD = len(df)
    
    # 3. Aggregated Metrics
    avg_yield = df['Yield_Percentage'].mean()
    total_defects = df['Defect_Count'].sum()
    failed_wafers = len(df[df['Yield_Percentage'] < 90])
    
    # 4. Create Workbook
    os.makedirs('excel', exist_ok=True)
    workbook = xlsxwriter.Workbook('excel/Cost_of_Quality_Analysis.xlsx')
    sheet = workbook.add_worksheet('Cost Analysis')
    
    # Formats
    title_fmt = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#2F5597'})
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#DDEBF7', 'border': 1})
    money_fmt = workbook.add_format({'num_format': '$#,##0', 'border': 1})
    pct_fmt = workbook.add_format({'num_format': '0.0%', 'border': 1})
    border_fmt = workbook.add_format({'border': 1})

    # Header
    sheet.write('A1', 'Semiconductor Fabrication - Cost of Quality Analysis', title_fmt)
    sheet.write('A3', 'Key Performance Indicators (KPIs)', header_fmt)
    
    kpis = [
        ['Total Wafers Produced', TOTAL_PROD],
        ['Average Fab Yield', avg_yield / 100],
        ['Total Defective Wafers', failed_wafers],
        ['Production Target (Ideal)', 6000]
    ]
    
    row = 3
    for kpi, val in kpis:
        sheet.write(row, 0, kpi, border_fmt)
        if 'Yield' in kpi:
            sheet.write(row, 1, val, pct_fmt)
        else:
            sheet.write(row, 1, val, border_fmt)
        row += 1

    # Financial Impact
    sheet.write('D3', 'Financial Loss Estimation', header_fmt)
    sheet.write('E3', 'Annualized Impact', header_fmt)
    
    scrap_loss = failed_wafers * (COST_PER_WAFER - SCRAP_VAL)
    yield_drop_impact = (TOTAL_PROD * 0.01) * COST_PER_WAFER # 1% yield drop cost
    
    fin_impact = [
        ['Total Scrap Cost', scrap_loss],
        ['Rework/Quality Loss', failed_wafers * 0.2 * REWORK_COST],
        ['Cost of 1% Yield Drop', yield_drop_impact],
        ['Total Quality Loss', scrap_loss + (failed_wafers * 0.2 * REWORK_COST)]
    ]
    
    row = 3
    for item, cost in fin_impact:
        sheet.write(row, 3, item, border_fmt)
        sheet.write(row, 4, cost, money_fmt)
        row += 1

    # Add a simple Column Chart
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'name':       'Loss Components',
        'categories': ['Cost Analysis', 3, 3, 6, 3],
        'values':     ['Cost Analysis', 3, 4, 6, 4],
        'fill':       {'color': '#4472C4'}
    })
    chart.set_title({'name': 'Financial Impact Analysis'})
    sheet.insert_chart('A10', chart)

    workbook.close()
    print("Excel report generated: excel/Cost_of_Quality_Analysis.xlsx")
    conn.close()

if __name__ == "__main__":
    generate_cost_of_quality_report()
