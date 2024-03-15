from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from models.account import Account
from models.user import User
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from validations.account_schema import account_schema
from cerberus import Validator
from random import randint


account_routes = Blueprint('account_routes', __name__)

Session = sessionmaker(bind=engine)

@account_routes.route("/users/<int:user_id>/accounts", methods=['GET'])
@login_required
def get_accounts(user_id):

    response_data = dict()

    try:
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        accounts = session.query(Account).filter(Account.user_id == user_id).all()
        response_data = {"accounts": [account.serialize() for account in accounts]}
        return jsonify(response_data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error Processing Data"}), 500
    finally:
        session.close()

@account_routes.route("/users/<int:user_id>/accounts/<int:account_id>", methods=['GET'])
@login_required
def get_account(user_id, account_id):

    try:

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        account = session.query(Account).filter(Account.account_id == account_id, Account.user_id == user_id).first()
        if not account:
            return jsonify({"message": "Account not found"}), 404
        return jsonify({"account": account.serialize()})
    
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": "Error Processing Data"}), 500
    finally:
        session.close()

@account_routes.route("/users/<int:user_id>/accounts", methods=['POST'])
@login_required
def create_account(user_id):

    v = Validator(account_schema)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON Data"}), 400
    
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    try:

        existing_account_numbers = [account.account_number for account in session.query(Account).all()]
        account_number = generate_unique_account_number(existing_account_numbers)
        existing_account = session.query(Account).filter(Account.user_id == user_id, Account.account_number == json_data['account_number']).first()
        if existing_account:
            return jsonify({"error": "Account number already exists"}), 400

        new_account = Account(
            user_id=current_user.user_id,
            account_type=json_data['account_type'],
            account_number=account_number,
            balance=json_data['balance']
        )
        print(new_account)
        session.add(new_account)
        session.commit()
        return jsonify({"message": "Success insert data"}), 201
    except IntegrityError as e:
        session.rollback()
        print(e)
        return jsonify({"message": "Duplicate account number"}), 409

    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"message": "Fail to insert data"}), 500
    finally:
        session.close()

def generate_unique_account_number(existing_account_numbers):
    while True:

        account_number = f'{randint(10000, 99999)}'

        if account_number not in existing_account_numbers:
            return account_number

@account_routes.route("/users/<int:user_id>/accounts/<int:account_id>", methods=['PUT'])
@login_required
def update_account(user_id, account_id):
    v = Validator(account_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    try:
        session = Session()
        account = session.query(Account).filter(Account.user_id == user_id, Account.account_id == account_id).first()
        if not account:
            return jsonify({"message": "Account not found"}), 404

        account.account_type = json_data['account_type']
        account.account_number = json_data['account_number']
        account.balance = json_data['balance']
        session.commit()
        return jsonify({"message": "Success updating data"})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"message": "Fail to update data"}), 500
    finally:
        session.close()

@account_routes.route("/users/<int:user_id>/accounts/<int:account_id>", methods=['DELETE'])
@login_required
def delete_account(user_id, account_id):
    try:
        session = Session()
        account = session.query(Account).filter(Account.user_id == user_id, Account.account_id == account_id).first()
        if not account:
            return jsonify({"message": "Account not found"}), 404

        session.delete(account)
        session.commit()
        return jsonify({"message": "Success delete data"})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"message": "Fail to delete data"}), 500
    finally:
        session.close()
