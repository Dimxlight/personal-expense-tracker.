from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'expenses.json'

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

def calculate_summary(expenses):
    summary = {}
    total = 0
    for expense in expenses:
        category = expense['category']
        amount = float(expense['amount'])
        total += amount
        summary[category] = summary.get(category, 0) + amount
    return summary, total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expenses = load_expenses()
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')

        expenses.append({
            'amount': amount,
            'category': category,
            'date': date
        })
        save_expenses(expenses)
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/summary')
def view_summary():
    expenses = load_expenses()
    summary, total = calculate_summary(expenses)
    return render_template('view_summary.html', expenses=expenses, summary=summary, total=total)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
