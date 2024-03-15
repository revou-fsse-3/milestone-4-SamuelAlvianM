from sqlite3 import IntegrityError
from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.orm import sessionmaker
from connectors.mysql_connector import engine

from models.transaction import Transaction
from models.account import Account
from validations.transaction_schema import transaction_schema

from sqlalchemy import select, or_
from cerberus import Validator
from flask_login import current_user, login_required

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route("/users/<int:user_id>/accounts/<int:account_id>/transactions", methods=['GET'])
@login_required
def get_transactions(user_id, account_id):
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        transactions = session.query(Transaction).filter(
            (Transaction.from_account_id == account_id) | (Transaction.to_account_id == account_id)
        ).all()
        response_data = {"transactions": [transaction.serialize() for transaction in transactions]}

        return jsonify(response_data), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong when fetching transactions"}), 500
    finally:
        session.close()

@transaction_routes.route("/users/<int:user_id>/accounts/<int:account_id>/transactions/<int:transaction_id>", methods=['GET'])
@login_required
def get_transaction_by_id(user_id, account_id, transaction_id):
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        transaction = session.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        if transaction is None:
            return jsonify({"message": "Transaction not found"}), 404
        response_data['transaction'] = transaction.serialize()

    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong when fetching transaction"}), 500

    finally:
        session.close()

    return jsonify(response_data)

@transaction_routes.route("/users/<int:user_id>/accounts/<int:account_id>/transactions", methods=['POST'])
@login_required
def create_transaction(user_id, account_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        data = request.json
        v = Validator(transaction_schema)
        if not v.validate(data):
            return jsonify({"error": v.errors}), 400

 
        from_account = session.query(Account).filter(Account.account_id == data['from_account_id']).first()
        to_account = session.query(Account).filter(Account.account_id == data['to_account_id']).first()


        if not from_account or not to_account:
            return jsonify({"error": "One or both of the accounts do not exist"}), 404


        new_transaction = Transaction(
            from_account_id=data['from_account_id'],
            to_account_id=data['to_account_id'],
            type_transaction=data['type_transaction'],
            amount=data['amount'],
            description=data['description']
        )

        session.add(new_transaction)
        session.commit()

        return jsonify({"message": "Transaction created successfully", 
                        "transaction_id": new_transaction.transaction_id}), 201
    
    except IntegrityError as e:
        session.rollback()
        print(e)
        return jsonify({"message": "Duplicate transaction"}), 409

    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to create transaction"}), 500
    
    finally:
        session.close()