import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

st.title("📈 Stock Analysis Dashboard")
st.write("Upload a CSV File of any stock (Standard format: Date, Open, High, Low, Close, Adj Close, Volume)")

# 1. FILE UPLOADER
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # 2. DATA LOADING & PREPROCESSING
    stock_df = pd.read_csv(uploaded_file)
    
    # Handling mixed date formats and sorting
    stock_df['Date'] = pd.to_datetime(stock_df['Date'], format='mixed')
    stock_df = stock_df.sort_values('Date').reset_index(drop=True)

    # Calculations
    # Formula: Daily Return = ((Current Adj Close - Previous Adj Close) / Previous Adj Close) * 100
    stock_df['Daily Return'] = stock_df['Adj Close'].pct_change() * 100

    # Formula: Cumulative Return = Product of (1 + Daily Return / 100)
    stock_df['Cumulative Return'] = (1 + stock_df['Daily Return'] / 100).cumprod()

    def percentage_return_classifier(percentage_return):
        if -0.3 < percentage_return <= 0.3: return 'Insignificant Change'
        elif 0.3 < percentage_return <= 3: return 'Positive Change'
        elif -3 < percentage_return <= -0.3: return 'Negative Change'
        elif 3 < percentage_return <= 7: return 'Large Positive Change'
        elif -7 < percentage_return <= -3: return 'Large Negative Change'
        elif percentage_return > 7: return 'Bull Run'
        elif percentage_return <= -7: return 'Bear Sell Off'
        return 'Stable'

    stock_df['Trend'] = stock_df['Daily Return'].apply(percentage_return_classifier)
    stock_df.dropna(subset=['Daily Return'], inplace=True)

    # 3. ACTION BUTTON
    if st.button('Generate Visualizations!'):
        
        st.divider()
        
        # Style Constants
        FONT_STYLE = dict(family="Montserrat, sans-serif", size=14)

        # --- VIZ 1: FILTERABLE PRICE LINE GRAPH ---
        st.subheader("1. Historical Price Analysis")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['Adj Close'], 
                                 line=dict(color='#1f77b4', width=2.5), name='Adj Close'))
        fig1.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                type="date"
            ),
            yaxis_title="Price ($)",
            template='plotly_white',
            font=FONT_STYLE
        )
        st.plotly_chart(fig1, use_container_width=True)

        # --- VIZ 2: TREND SUMMARY PIE CHART ---
        st.subheader("2. Return Trend Distribution")
        trend_summary = stock_df['Trend'].value_counts()
        fig2 = px.pie(
            names=trend_summary.index, 
            values=trend_summary.values, 
            color_discrete_sequence=px.colors.qualitative.Prism,
            hole=0.4
        )
        fig2.update_layout(template='plotly_white', font=FONT_STYLE)
        st.plotly_chart(fig2, use_container_width=True)

        # --- VIZ 3: CANDLESTICK CHART ---
        st.subheader("3. Candlestick Price Action")
        fig3 = go.Figure(data=[go.Candlestick(
            x=stock_df['Date'],
            open=stock_df['Open'], high=stock_df['High'],
            low=stock_df['Low'], close=stock_df['Close'],
            increasing_line_color='#2ca02c', decreasing_line_color='#d62728'
        )])
        fig3.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_white',
            font=FONT_STYLE,
            yaxis_title="Price ($)"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # --- VIZ 4: VOLUME VS PRICE SCATTERPLOT ---
        st.subheader("4. Volume vs. Adjusted Close")
        fig4 = px.scatter(
            stock_df, x='Volume', y='Adj Close', color='Trend',
            labels={'Adj Close': 'Price ($)', 'Volume': 'Volume'},
            opacity=0.6,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig4.update_layout(template='plotly_white', font=FONT_STYLE)
        st.plotly_chart(fig4, use_container_width=True)

        # --- VIZ 5: CUMULATIVE RETURNS ---
        st.subheader("5. Cumulative Returns (Growth of $1)")
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['Cumulative Return'], 
                                 line=dict(color='#2ca02c', width=2), 
                                 fill='tozeroy', fillcolor='rgba(44, 160, 44, 0.1)',
                                 name='Cumulative Return'))
        fig5.update_layout(
            yaxis_title="Investment Value ($)",
            template='plotly_white',
            font=FONT_STYLE
        )
        st.plotly_chart(fig5, use_container_width=True)

else:
    st.info("Please upload a CSV file in the correct format to get started.")
