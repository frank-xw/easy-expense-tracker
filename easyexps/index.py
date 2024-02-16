from flask import Flask, jsonify, request

from easyexps.model.expense import Expense, ExpenseSchema
from easyexps.model.income import Income, IncomeSchema
from easyexps.model.transaction_type import TransactionType
from easyexps.model.transaction import TransactionSchema

from easyexps.secure.auth import AuthError, requires_auth, requires_scope

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
@requires_auth
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
@requires_auth
def add_expenses():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return '', 204


@app.route('/api/transactions')
@requires_auth
def get_transactions():
    if requires_scope("read:admin"):
        schema = TransactionSchema(many=True)
        all_trans = schema.dump(transactions)
        return jsonify(all_trans)

    raise AuthError({
        "code": "Unauthorized",
        "description": "This resource needs admin scope"
    }, 403)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == "__main__":
    app.run()
