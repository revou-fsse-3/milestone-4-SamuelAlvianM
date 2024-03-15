from datetime import datetime
from sqlite3 import IntegrityError
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from connectors.mysql_connector import engine
from models.user import User
from sqlalchemy.orm import sessionmaker
from cerberus import Validator
from validations.user_schema import user_schema

user_routes_register = Blueprint('user_routes_register',__name__)

@user_routes_register.route("/register", methods=['GET'])
def user_register():
    return render_template("users/register.html")

@user_routes_register.route("/register", methods=['POST'])
def do_registration():

    v = Validator(user_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    username = json_data['username']
    email = json_data['email']
    password = json_data['password']

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return "Already have Account, go to LOGIN"
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    new_user.created_at = datetime.now()

    try:
        session.add(new_user)
        session.commit()
        return redirect(url_for('user_routes_login.user_login')) 
    except IntegrityError:
        session.rollback()
        return "Failed to register user. Please try again."
    finally:
        session.close()