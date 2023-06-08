from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

df = pd.read_csv('data/s&p500_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

X = df['Year'].values.reshape(-1, 1).astype(float)
y = df['Open']

model = LinearRegression()
model.fit(X, y)

@app.route('/', methods=['GET'])
def index():
    return render_template('linear_index.html')

@app.route('/calculate_growth', methods=['POST'])
def calculate_growth():
    initial_investment = float(request.form['investment'])
    current_year = df['Year'].max()
    future_years = range(current_year + 1, current_year + 11)  # Predicting for the next 10 years
    future_X = pd.DataFrame(future_years, columns=['Year'])
    future_y_pred = model.predict(future_X)

    future_dates = pd.date_range(start='2023-05-01', periods=10, freq='AS')
    
    current_price = df.loc[df['Year'] == current_year, 'Open'].values[0]
    growth_rates = future_y_pred / current_price

    future_values = [initial_investment * (1 + growth) for growth in growth_rates]

    result = [{'date': date.strftime('%Y-%m-%d'), 'value': value} for date, value in zip(future_dates, future_values)]
    return render_template('linear_result.html', result=result)


@app.route('/result', methods=['POST'])
def result():
    return render_template('linear_result.html')

if __name__ == '__main__':
    app.run()
