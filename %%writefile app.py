%%writefile app.py
import streamlit as st
from pickle import load
import pandas as pd

# Load the saved Holt-Winters model
with open("fina.sav", "rb") as file:
    hwe_model_add_add = load(file)

# Load historical price data
df = pd.read_csv("/content/Gold_data.csv")

# Function to make predictions using the loaded model
def predict(start_date, periods):
    # Perform forecasting
    forecast = hwe_model_add_add.forecast(steps=periods)

    # Get the last observed value before differencing
    last_observed_value = df["price"].iloc[-1]

    # Cumulatively sum the forecasted differences to the last observed value
    forecast = forecast.cumsum() + last_observed_value

    # Create date range for the forecasted dates
    forecast_dates = pd.date_range(start=start_date, periods=periods, freq='D')

    return forecast_dates, forecast

# Streamlit app
def main():
    # Add CSS for background image
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('/content/Blog_Paytm_Gold-Rates-Historical-Data-for-India-800x500.jpg') no-repeat center center fixed;
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Gold Price Prediction")
    st.sidebar.title("Navigation")

    # Add input parameters in the sidebar
    start_date = st.sidebar.date_input("Start Date", value=pd.Timestamp.now())


    # Set periods to forecast for 10 days
    periods = 15
    # Add subheader for predictions
    st.subheader("Predictions")

    # Predict and display the result
    if st.sidebar.button("Forecast"):
        forecast_dates, forecast_prices = predict(start_date, periods)
        for date, price in zip(forecast_dates, forecast_prices):
            st.write(f"<span style='font-weight:bold; color:blue;'>Date:</span> <span style='color:black;'>{date.date()}</span>, <span style='font-weight:bold; color:red;'>Predicted Price:</span> <span style='color:black;'>{price}</span>", unsafe_allow_html=True)

# Display image related to gold prices
st.image("/content/Blog_Paytm_Gold-Rates-Historical-Data-for-India-800x500.jpg", use_column_width=True)



if __name__ == "__main__":
    main()
