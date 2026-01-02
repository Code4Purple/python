from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import os
from datetime import datetime
from collections import defaultdict
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to a random secret key

# File paths
USERS_FILE = 'users.dat'
TRANSACTIONS_FILE = 'transactions.dat'

# Initialize data files
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'wb') as f:
            pickle.dump({}, f)
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'wb') as f:
            pickle.dump([], f)

def load_users():
    try:
        with open(USERS_FILE, 'rb') as f:
            return pickle.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'wb') as f:
        pickle.dump(users, f)

def load_transactions():
    try:
        with open(TRANSACTIONS_FILE, 'rb') as f:
            return pickle.load(f)
    except:
        return []

def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, 'wb') as f:
        pickle.dump(transactions, f)

def get_monthly_data(month, year):
    transactions = load_transactions()
    username = session.get('username')
    
    income = 0
    expenses = 0
    monthly_transactions = []
    
    for t in transactions:
        if t['username'] == username:
            t_date = datetime.strptime(t['date'], '%Y-%m-%d')
            if t_date.month == month and t_date.year == year:
                monthly_transactions.append(t)
                if t['type'] == 'income':
                    income += t['amount']
                else:
                    expenses += t['amount']
    
    return {
        'income': income,
        'expenses': expenses,
        'transactions': sorted(monthly_transactions, key=lambda x: x['date'], reverse=True)
    }

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_users()
        
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        users = load_users()
        
        if username in users:
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        users[username] = generate_password_hash(password)
        save_users(users)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    now = datetime.now()
    data = get_monthly_data(now.month, now.year)
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         month=now.strftime('%B %Y'),
                         income=data['income'],
                         expenses=data['expenses'],
                         balance=data['income'] - data['expenses'],
                         transactions=data['transactions'][:5])

@app.route('/transactions')
def transactions():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    now = datetime.now()
    month = request.args.get('month', now.month, type=int)
    year = request.args.get('year', now.year, type=int)
    
    data = get_monthly_data(month, year)
    
    return render_template('transactions.html',
                         username=session['username'],
                         month=datetime(year, month, 1).strftime('%B %Y'),
                         month_num=month,
                         year=year,
                         transactions=data['transactions'],
                         income=data['income'],
                         expenses=data['expenses'])

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    try:
        transactions = load_transactions()
        
        new_transaction = {
            'username': session['username'],
            'date': request.form.get('date'),
            'time': request.form.get('time', datetime.now().strftime('%H:%M:%S')),
            'name': request.form.get('name'),
            'amount': float(request.form.get('amount')),
            'type': request.form.get('type'),
            'id': len(transactions)
        }
        
        transactions.append(new_transaction)
        save_transactions(transactions)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'username' not in session:
        return jsonify({'success': False})
    
    transactions = load_transactions()
    transactions = [t for t in transactions if t.get('id') != transaction_id or t['username'] != session['username']]
    save_transactions(transactions)
    
    return jsonify({'success': True})

@app.route('/upload_transactions', methods=['POST'])
def upload_transactions():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    try:
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')
        
        transactions = load_transactions()
        added = 0
        
        for line in lines:
            if not line.strip():
                continue
            
            # Expected format: date,time,name,amount,type
            # Example: 2024-01-15,14:30:00,Grocery Store,45.50,expense
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) >= 4:
                new_transaction = {
                    'username': session['username'],
                    'date': parts[0],
                    'time': parts[1] if len(parts) > 4 else '00:00:00',
                    'name': parts[2] if len(parts) > 4 else parts[1],
                    'amount': float(parts[3] if len(parts) > 4 else parts[2]),
                    'type': parts[4] if len(parts) > 4 else parts[3],
                    'id': len(transactions) + added
                }
                transactions.append(new_transaction)
                added += 1
        
        save_transactions(transactions)
        return jsonify({'success': True, 'message': f'Added {added} transactions'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/monthly_chart_data')
def monthly_chart_data():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'})
    
    now = datetime.now()
    data = get_monthly_data(now.month, now.year)
    
    # Group by day
    daily_income = defaultdict(float)
    daily_expenses = defaultdict(float)
    
    for t in data['transactions']:
        day = datetime.strptime(t['date'], '%Y-%m-%d').day
        if t['type'] == 'income':
            daily_income[day] += t['amount']
        else:
            daily_expenses[day] += t['amount']
    
    days = list(range(1, 32))
    income_data = [daily_income.get(d, 0) for d in days]
    expense_data = [daily_expenses.get(d, 0) for d in days]
    
    return jsonify({
        'days': days,
        'income': income_data,
        'expenses': expense_data
    })

if __name__ == '__main__':
    init_files()
    app.run(debug=True, host='0.0.0.0', port=5000)