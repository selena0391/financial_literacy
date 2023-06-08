from flask import Flask, render_template, request
import csv
from datetime import datetime
#import matplotlib.pyplot as plt
import io
import base64
from sklearn.linear_model import LinearRegression
import pandas as pd

app = Flask(__name__)
print(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/index.html')
def start():
    return render_template('index.html')




@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contacts.html')
def contact():
    return render_template('contacts.html')


@app.route('/learn.html')
def learn():
    return render_template('learn.html')

# Route for handling form submission
@app.route('/simulate', methods=['POST'])
def simulate():
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()
    money_invested = float(request.form['money_invested'])

    # Read the CSV file
    data = []
    with open('data/s&p500_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
            if start_date <= date <= end_date:
                data.append({
                    'date': date,
                    'open': float(row['Open']),
                    'close': float(row['Close'])
                })

    # Perform the simulation trading logic
    portfolio_value = money_invested
    trades = 0
    for i in range(len(data) - 1):
        current_price = data[i]['close']
        next_price = data[i + 1]['open']
        if next_price > current_price:
            # Buy
            shares_to_buy = portfolio_value / current_price
            portfolio_value = shares_to_buy * next_price
            trades += 1

    # Convert portfolio value to a dollar amount with 2 decimal places
    portfolio_value = round(portfolio_value, 2)

    # Calculate the percentage change
    percent_change = ((portfolio_value - money_invested) / money_invested) * 100

    # Calculate the current value
    current_value = portfolio_value

    # Construct the simulation result
    simulation_result = {
        'start_date': start_date,
        'end_date': end_date,
        'money_invested': money_invested,
        'portfolio_value': portfolio_value,
        'trades': trades,
        'percent_change': percent_change,
        'current_value': current_value
    }

    return render_template('result.html', result=simulation_result)

@app.route('/budget.html')
def budget():
    return render_template('budget.html')

@app.route('/calculate', methods = ['POST'])
def calculate():

    # Input income

    income = float(request.form['income'])

    # Input expenses

    gas = float(request.form['gas'])
    groceries = float(request.form['groceries'])
    rent_mortgage = float(request.form['rent_mortgage'])
    utilities = float(request.form['utilities'])
    miscellaneous = float(request.form['miscellaneous'])

    # Calculate total expenses

    total_expenses = gas + groceries + rent_mortgage + utilities + miscellaneous

    # Calculate available funds for investment

    available_funds = income - total_expenses

    # Define investment percentage

    investment_percentage = 0.2

    # Calculate investment amount

    investment_amount = available_funds * investment_percentage
    # Generate the histogram

    #labels = ['Expenses', 'Available Funds', 'Investment Amount']
    #amounts = [total_expenses, available_funds, investment_amount]
    #colors = ['red', 'green', 'blue']

    #plt.bar(labels, amounts, color = colors)
    #plt.xlabel('Categories')
    #plt.ylabel('Amount')
    #plt.title('Expense Breakdown')

    # Convert the plot to base64 for embedding in HTML

    #buffer = io.BytesIO()
    #plt.savefig(buffer, format = 'png')
    #buffer.seek(0)
    #image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    #buffer.close()
    result = {
        'investment_amount': investment_amount}

    return render_template('result_2.html', result=result) #image_base64=image_base64)




df = pd.read_csv('data/s&p500_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

X = df['Year'].values.reshape(-1, 1).astype(float)
y = df['Open']

model = LinearRegression()
model.fit(X, y)

@app.route('/linear_index.html', methods=['GET'])
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
    app.run(debug=True)

