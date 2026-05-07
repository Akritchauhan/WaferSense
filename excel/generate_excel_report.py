import pandas as pd
import numpy as np
import xlsxwriter
import sqlite3

def generate_excel():
    print("Generating Corporate Excel Financial Report...")
    conn = sqlite3.connect('wafersense.db')
    df = pd.read_sql_query("SELECT * FROM wafers", conn)
    
    # Financial Constants
    COST_PER_WAFER = 500  # Manufacturing cost
    SCRAP_VALUE = 50      # Recoverable scrap value
    REWORK_COST = 150     # Cost to fix minor defects
    
    # Aggregated Data for Financials
    total_wafers = len(df)
    avg_yield = df['Yield_Percentage'].mean()
    failed_wafers = len(df[df['Yield_Percentage'] < 90])
    
    workbook = xlsxwriter.Workbook('excel/Cost_of_Quality_Analysis.xlsx')
    worksheet = workbook.add_worksheet('Financial Impact')
    
    # Formatting
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'border': 1})
    money_fmt = workbook.add_format({'num_format': '$#,##0', 'border': 1})
    pct_fmt = workbook.add_format({'num_format': '0.00%', 'border': 1})
    border_fmt = workbook.add_format({'border': 1})

    # Summary Section
    worksheet.write('A1', 'Semiconductor Fabrication - Cost of Quality Analysis', workbook.add_format({'bold': True, 'font_size': 14}))
    
    headers = ['Metric', 'Value']
    data = [
        ['Total Wafers Processed', total_wafers],
        ['Average Yield %', avg_yield / 100],
        ['Total Failed Wafers', failed_wafers],
        ['Yield Loss (Estimated)', (1 - avg_yield/100) * total_wafers]
    ]
    
    row = 3
    for h in headers:
        worksheet.write(row, headers.index(h), h, header_fmt)
    
    row += 1
    for item, val in data:
        worksheet.write(row, 0, item, border_fmt)
        if 'Yield' in item:
            worksheet.write(row, 1, val, pct_fmt)
        else:
            worksheet.write(row, 1, val, border_fmt)
        row += 1

    # Financial Impact Calculations
    worksheet.write('D3', 'Financial Projections (Annualized)', header_fmt)
    worksheet.write('E3', 'Amount', header_fmt)
    
    scrap_cost = failed_wafers * (COST_PER_WAFER - SCRAP_VALUE)
    potential_revenue_loss = (100 - avg_yield) * total_wafers * 50 # Arbitrary loss factor
    
    fin_data = [
        ['Estimated Scrap Cost', scrap_cost],
        ['Rework Expenses', failed_wafers * 0.3 * REWORK_COST],
        ['Total Quality Loss', scrap_cost + (failed_wafers * 0.3 * REWORK_COST)],
        ['Impact per 1% Yield Drop', total_wafers * 0.01 * COST_PER_WAFER]
    ]
    
    row = 4
    for item, val in fin_data:
        worksheet.write(row, 3, item, border_fmt)
        worksheet.write(row, 4, val, money_fmt)
        row += 1

    # Charts
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'name': 'Financial Loss by Category',
        'categories': ['Financial Impact', 4, 3, 7, 3],
        'values':     ['Financial Impact', 4, 4, 7, 4],
    })
    worksheet.insert_chart('A15', chart)

    workbook.close()
    print("Excel report 'Cost_of_Quality_Analysis.xlsx' generated successfully.")
    conn.close()

if __name__ == "__main__":
    generate_excel()
