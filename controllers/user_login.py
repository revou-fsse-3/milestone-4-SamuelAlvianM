# routes/user.py

from flask import Blueprint, jsonify, render_template, request, redirect
from connectors.mysql_connector import engine
from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token

user_routes_login = Blueprint('user_routes_login', __name__)

@user_routes_login.route("/login", methods=['GET'])
def user_login():
    return render_template("users/login.html")

@user_routes_login.route("/login", methods=['POST'])
def do_user_login():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = session.query(User).filter(User.email == email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if not user.check_password(password):
            return jsonify({"message": "Incorrect password"}), 401

        login_user(user, remember=False)
        return redirect(f'/users/{user.user_id}')

    except Exception as e:
        return jsonify({"message": f"Login Failed: {str(e)}"}), 500

@user_routes_login.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/')

@user_routes_login.route("/loginjwt", methods=['POST'])
def user_login_jwt():
    connection = engine.connect()
    Session = sessionmaker(bind=connection)
    session = Session()

    try:
        user = session.query(User).filter(User.email == request.form['email']).first()

        if user is None:
            return jsonify({"message": "Email tidak terdaftar"}), 404

        if not user.check_password(request.form['password']):
            return jsonify({"message": "Wrong Password"}), 401

        access_token = create_access_token(identity=user.user_id, additional_claims={"username": user.username})
        return jsonify({'access_token': access_token})

    except Exception as e:
        return jsonify({"message": "Login Failed"}), 500
