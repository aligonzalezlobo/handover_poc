 # Client Analytics and Financial Planning Tool

This Streamlit application is designed to provide sales teams with powerful insights into customer behavior, risk of churn, and financial planning capabilities. It features several interactive tools to empower sales professionals to make informed decisions, strategize customer retention, and effectively allocate budget resources.

## Features

- **Home Page**: Offers an overview of the application and its purpose, including basic statistics about the total number of clients, total sales, and net revenue.

- **AI Client Ranking**: Allows users to rank clients based on various metrics such as churn probability, total sales return, and priority score. Users can filter clients by branch and client type, and sort the list based on the selected metric.

- **Client Deep-Dive**: Provides detailed analytics for individual clients, including frequency of orders, last order date, number of returns, and preferred way of contact. It also features a time series graph of sales net over time.

- **Financial Tool**: Enables the sales team to input an available budget and project potential sales recovery. The tool prioritizes clients based on a provided budget and preferred method of contact, displaying the number of clients that can be contacted and the expected return.

## Data

The application uses several CSV data files:

- `final_data2.csv`: Contains overall sales and client data.
- `top_client_data.csv`: Includes time-series data for sales analysis.
- `financial_tool.csv`: Used in the financial tool for budget allocation and client prioritization.

## Usage

To run the application, navigate to the app's directory in your terminal and execute:

```bash
streamlit run app.py