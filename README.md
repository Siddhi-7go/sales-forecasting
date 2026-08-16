# Sales Forecasting Using Time Series Analysis

## Project Overview
This project forecasts future sales using historical retail sales data. The workflow covers data cleaning, exploratory data analysis, time-series decomposition, stationarity testing, forecasting models, evaluation, and future prediction.

## Dataset
The project uses the Superstore dataset supplied with the internship Week 1 material. The main fields used for forecasting are `Order Date` and `Sales`; other fields such as Category, Region, Quantity, Discount, and Profit are used for supporting EDA.

## Objectives
- Understand historical sales patterns.
- Identify trend and seasonality.
- Test time-series stationarity using the Augmented Dickey-Fuller test.
- Examine ACF and PACF.
- Compare forecasting approaches.
- Select a suitable model using MAE, RMSE, and MAPE.
- Forecast future monthly sales.

## Models
- Naive baseline
- Simple Exponential Smoothing
- Holt's Linear Trend
- Holt-Winters Exponential Smoothing
- ARIMA
- SARIMA

## Project Structure
```text
Sales_Forecasting_Project/
├── data/
│   └── Superstore.xlsx
├── notebooks/
│   └── Sales_Forecasting.ipynb
├── outputs/
├── app.py
├── requirements.txt
└── README.md
```

## Installation
Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

## Run the Notebook
```bash
jupyter notebook
```
Open `notebooks/Sales_Forecasting.ipynb` and run the cells from top to bottom.

## Run the Dashboard
From the project root:

```bash
streamlit run app.py
```

## Evaluation Metrics
- **MAE:** Mean Absolute Error
- **RMSE:** Root Mean Squared Error
- **MAPE:** Mean Absolute Percentage Error

Lower values indicate better forecasting performance.

## Important Note
The final model and its numerical results must be reported from the actual notebook execution. Do not copy example metrics from tutorials.

## Author
**[Your Name]**  
Data Science Internship Project
