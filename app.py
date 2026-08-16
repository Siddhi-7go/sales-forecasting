import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title='Sales Forecasting', page_icon='📈', layout='wide')
st.title('📈 Sales Forecasting Dashboard')
st.caption('Sales Forecasting Using Time Series Analysis')

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file)
    return pd.read_excel('data/Superstore.xlsx')

uploaded = st.sidebar.file_uploader('Upload Superstore Excel file (optional)', type=['xlsx', 'xls'])
df = load_data(uploaded)

df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df = df.dropna(subset=['Order Date', 'Sales']).sort_values('Order Date')

st.sidebar.header('Forecast Settings')
model_name = st.sidebar.selectbox('Model', ['Holt-Winters', 'SARIMA'])
horizon = st.sidebar.slider('Future months', 3, 24, 12)

monthly_sales = df.set_index('Order Date')['Sales'].resample('MS').sum()

c1, c2, c3 = st.columns(3)
c1.metric('Total Sales', f"${df['Sales'].sum():,.2f}")
c2.metric('Orders', f"{df['Order ID'].nunique():,}" if 'Order ID' in df.columns else f"{len(df):,}")
c3.metric('Months', f"{len(monthly_sales):,}")

st.subheader('Historical Monthly Sales')
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(monthly_sales.index, monthly_sales.values)
ax.set_xlabel('Date')
ax.set_ylabel('Sales')
ax.set_title('Monthly Sales Trend')
ax.grid(alpha=0.25)
st.pyplot(fig)
plt.close(fig)

if len(monthly_sales) < 24:
    st.error('At least 24 monthly observations are recommended for this forecasting dashboard.')
    st.stop()

if model_name == 'Holt-Winters':
    model = ExponentialSmoothing(monthly_sales, trend='add', seasonal='add', seasonal_periods=12)
    fit = model.fit(optimized=True)
    forecast = fit.forecast(horizon)
else:
    model = SARIMAX(monthly_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                    enforce_stationarity=False, enforce_invertibility=False)
    fit = model.fit(disp=False)
    forecast = fit.get_forecast(steps=horizon).predicted_mean

st.subheader(f'{model_name} Future Forecast')
forecast_df = pd.DataFrame({'Forecast Sales': forecast})
st.dataframe(forecast_df.style.format('${:,.2f}'), use_container_width=True)

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(monthly_sales.index, monthly_sales.values, label='Historical Sales')
ax2.plot(forecast.index, forecast.values, label='Forecast')
ax2.axvline(monthly_sales.index[-1], linestyle='--', alpha=0.6)
ax2.set_xlabel('Date')
ax2.set_ylabel('Sales')
ax2.set_title(f'Historical Sales and {model_name} Forecast')
ax2.legend()
ax2.grid(alpha=0.25)
st.pyplot(fig2)
plt.close(fig2)

csv = forecast_df.to_csv().encode('utf-8')
st.download_button('Download Forecast CSV', csv, 'sales_forecast.csv', 'text/csv')
