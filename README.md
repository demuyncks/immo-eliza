# immo-eliza

# Real Estate Analysis: Belgium Market 2026

## 📝 Description

This project provides a comprehensive exploratory data analysis (EDA) of the Belgian real estate market. Using a dataset of over 13,000 properties, the analysis uncovers the key drivers of property prices, regional disparities, and market trends across **Brussels, Flanders, and Wallonia**.

**Key questions answered:**
What are the top 5 variables impacting property prices?
How does the price per square meter vary by region and property type?
Which are the most and least expensive municipalities in Belgium?
How are property surfaces distributed across different regions?

## ⚙️ Installation

To run this analysis locally, you need Python 3.8+ and the following libraries:
bash
pip install pandas matplotlib seaborn numpy
Use code with caution.

## 🚀 Usage

Clone the repository.
Ensure your cleaned dataset (e.g., df4) is available in the project folder.
Run the Jupyter notebook or Python script:
python

## Run the main analysis blocks


The script will generate visual plots and export a final report to Belgium_Real_Estate_Report.xlsx.

## 🖼️ Visuals

The project includes several high-impact visualizations:
**Correlation Heatmaps**: Proving that living_area (0.61) and location are the prime price drivers.
**FacetGrid Histograms**: Comparing surface distributions between Houses and Apartments across all 3 regions.
**Comparative Bar Charts**: Side-by-side analysis of Median Price vs. Price per SQM for the top municipalities.
**Boxplots**: Identifying luxury outliers and market spreads.

## 👥 Contributors

## ⏳ Timeline

Day 1: Data Cleaning, handling missing values (median/mode imputation).
Day 2: Outlier detection and feature engineering (price_sqm).
Day 3: Statistical analysis and Regional deep-dives.
Day 4: Final visualization and Reporting.

## 💡 Personal Situation

This project was developed as part of a Data Science bootcamp/challenge. The goal was to transform raw, messy real estate data into actionable insights. The most challenging part was synchronizing the "Garden/Terrace" flags with their respective areas and creating a robust filtering system to remove "trash" listings (e.g., 1€ auctions) without losing the high-end luxury segment.
