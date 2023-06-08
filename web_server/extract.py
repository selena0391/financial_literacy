import yfinance as yf

# Set the start and end dates for the historical data
start_date = '2000-01-01'
end_date = '2023-05-19'

# Fetch the S&P 500 data
snp500 = yf.download('^GSPC', start=start_date, end=end_date)

# Save the data to a CSV file
snp500.to_csv('s&p500_data.csv')
