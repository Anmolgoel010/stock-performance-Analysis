# Individual Stock Performance Analysis Project

A Python-based tool for analyzing individual stock performance using historical data. Just download any Historical stock dataset from Yahoo finanace, Google Finance etc and generate an insightful dashboard for visualization.

### Insights Provided:
From the raw stock data (CSV file), you will be able to get the following insights:
1. Historical Price Analysis.
2. Classification of daily returns based on categories like insignificant, positive, negative changes, etc. (visualized with a pie chart)
3. An interactive candlestick chart that explicitly mention open, close, high and low for each day.
4. A scatter plot showing the relationship between trading volume and closing prices of the particular stock.
5. A Cummulative line chart showing the growth of 1$ over the years.


1. Prerequisites
Ensure you have Python installed (version 3.8 or higher is recommended).

2. Install Required Libraries
Open your terminal or command prompt and run the following command to install the necessary dependencies:
pip install streamlit pandas numpy plotly

3. Prepare Your Data
The application accepts CSV files (like your WMT.csv) with the following standard columns:
-Date (Supports mixed formats like DD-MM-YYYY or M/D/YYYY)
-Open, High, Low, Close, Adj Close
-Volume

💻 How to Run the App
Save the application code as app.py.

-Navigate to the folder containing the file in your terminal.
-Launch the Streamlit server by running:
streamlit run app.py
-Your default web browser will open automatically to http://localhost:8501.
-Upload your CSV file and click the "Generate 5 Visualizations" button to view the dashboard.

📁 Project Structure
-app.py: The main Streamlit application script.
-README.md: Project documentation and setup guide.
-WMT.csv: (Optional) Example dataset for testing.

## License

This project is licensed under the **GNU AFFERO GENERAL PUBLIC LICENSE V3**.

:)
