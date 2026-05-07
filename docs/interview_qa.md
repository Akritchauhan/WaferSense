# Semiconductor Analytics Interview Preparation Guide

This document contains key technical and domain-specific questions related to this project that you may encounter in interviews for Data Analyst or Semiconductor Analyst roles.

## 1. Technical SQL Questions

**Q: Can you explain how you calculated the failure rate for each machine?**
*A: I used a CASE statement inside a SUM function to count wafers with a yield below 90%, then divided that by the total count of wafers for that machine ID. I cast the numerator to a float to ensure precise decimal division.*

**Q: Why are window functions useful in sensor analysis?**
*A: Window functions allow us to calculate moving averages or detect drift over time without collapsing the rows into a single group. This is critical for spotting when a machine starts to deviate from its normal operating range.*

## 2. Python & Statistical Analysis

**Q: What was the strongest correlation you found in the dataset?**
*A: The strongest correlation was between Chamber Pressure and Gate Oxide Thickness. Specifically, higher pressure was strongly correlated with thinner oxide layers, which directly led to higher defect counts.*

**Q: How did you handle missing or noisy sensor data?**
*A: I used the IQR (Interquartile Range) method to identify and remove outliers that were likely sensor malfunctions rather than real process variations. This ensured that our statistical models were based on reliable manufacturing data.*

## 3. Domain (Semiconductor) Questions

**Q: What is a 'Wafer Map' and why is it important?**
*A: A Wafer Map is a spatial visualization of defects across a circular wafer. It's important because defect patterns (like clusters at the edge or a ring in the middle) often point to specific equipment issues, such as uneven gas flow or heating element failure.*

**Q: What does 'Yield' mean in a semiconductor context?**
*A: Yield is the percentage of functional chips on a wafer compared to the total possible chips. Maximizing yield is the primary goal of fab analytics because even a 1% increase in yield can save millions of dollars in manufacturing costs.*

## 4. Financial & Business Impact

**Q: How did you calculate the 'Cost of Quality'?**
*A: I calculated the 'Scrap Cost' (Wafers that must be thrown away) and 'Rework Cost' (Wafers that can be fixed). I also estimated the revenue loss from a 1% yield drop based on the manufacturing cost per wafer, providing a clear financial justification for process improvements.*
