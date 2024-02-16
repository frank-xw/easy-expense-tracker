from flask import Flask, jsonify, request

from easyexps.model.expense import Expense, ExpenseSchema
from easyexps.model.income import Income, IncomeSchema
from easyexps.model.transaction_type import TransactionType


app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]


@app.route("/api/incomes")
def get_incomes():
    schema = IncomeSchema(many=True)  # Collection of object: set many to true
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes)


@app.route("/api/incomes", methods=['POST'])
def add_incomes():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return '', 204


@app.route('/api/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)  # Collection of object: set many to true
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)


@app.route('/api/expenses', methods=['POST'])
def add_expenses():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return '', 204


if __name__ == "__main__":
    app.run()
