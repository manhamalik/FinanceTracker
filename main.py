from flask import Flask, render_template, request

app = Flask(__name__)

transactions = []
expense_summary = {}


@app.route('/')
def index():
    show_summary = request.args.get('show_summary', False)
    return render_template('index.html', transactions=transactions, show_summary=show_summary, expense_summary=expense_summary)


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form['date']
    description = request.form['description']
    amount = request.form['amount']
    category = request.form['category']

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        error_message = 'Amount must be a positive number'
        return render_template('index.html', transactions=transactions, show_summary=False, expense_summary=expense_summary, error_message=error_message)

    transactions.append({
        'date': date,
        'description': description,
        'amount': amount,
        'category': category
    })

    if category in expense_summary:
        expense_summary[category] += amount
    else:
        expense_summary[category] = amount

    return render_template('index.html', transactions=transactions, show_summary=False, expense_summary=expense_summary)


@app.route('/show_summary', methods=['POST'])
def show_summary():
    return render_template('index.html', transactions=transactions, show_summary=True, expense_summary=expense_summary)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
