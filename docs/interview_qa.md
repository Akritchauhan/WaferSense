# Semiconductor Analytics Interview Preparation Guide

## 1. SQL Analytics
- **Joining Datasets:** Used `INNER JOIN` to link wafer yields with machine maintenance schedules.
- **Aggregations:** Utilized `GROUP BY` and `SUM` to calculate total defects per machine.
- **Logic:** Implemented `CASE` statements to categorize wafer batches based on yield performance (Excellent/Needs Attention).

## 2. Python Data Analysis
- **Data Cleaning:** Applied the **IQR (Interquartile Range)** method to remove sensor anomalies.
- **Correlation:** Found a strong correlation between **Chamber Pressure** and **Gate Oxide Thickness**, explaining why machine drift leads to defects.
- **Visualization:** Used **Seaborn** to create distribution plots and heatmaps for process stability monitoring.

## 3. Financial Impact
- **Cost of Quality:** Calculated the cost of scrapped wafers vs. the potential revenue gain from a 1% yield increase.
- **Scrap Cost:** Wafers failing the 90nm threshold result in significant material loss (est. $450/wafer).