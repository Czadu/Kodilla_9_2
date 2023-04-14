import requests
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']

csv_filename = 'rates_new.csv'
with open(csv_filename, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['currency', 'code', 'bid', 'ask'], delimiter=';')
    writer.writeheader()
    for rate in data[0]['rates']:
        writer.writerow(rate)

csv_filename = 'rates.csv'

exchange_rates = {}

with open(csv_filename) as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    for row in reader:
        currency = row[0]
        code = row[1]
        bid = float(row[2])
        ask = float(row[3])
        exchange_rates[code] = {
            'currency': currency,
            'bid': bid,
            'ask': ask,
        }

@app.route('/')
def index():
    return render_template('calculator.html', currencies=exchange_rates)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    currencies = []
    result = None
    for code, rate in exchange_rates.items():
        currencies.append(f"{rate['currency']} ({code})")
        if request.method == 'POST' and code == request.form['currency']:
            amount = float(request.form['amount'])
            rate_pln = float(rate['ask'])
            cost_pln = amount * rate_pln
            result = (round(cost_pln, 2))
    return render_template('calculator.html', currencies=currencies, result=result)