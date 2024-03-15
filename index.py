from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from connectors.mysql_connector import engine, connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


from flask_login import LoginManager, login_required
from flask_jwt_extended import JWTManager
from models.account import Account
from models.user import User
import os

# Load Controller Files
from controllers.accounts import account_routes
from controllers.user_register import user_routes_register
from controllers.user_login import user_routes_login
from controllers.transactions import transaction_routes
from controllers.users import users_route


load_dotenv()

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

# JWT
jwt = JWTManager(app)

# LOGIN SESSION
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(account_routes)
app.register_blueprint(user_routes_register)
app.register_blueprint(user_routes_login)
app.register_blueprint(transaction_routes)
app.register_blueprint(users_route)


# Product Route
@app.route("/")
def hello_world():
    
    account_query = select(Account)
    Session = sessionmaker(connection)
    with Session() as session:
        result = session.execute(account_query)
        for row in result.scalars():
            print(f'ID: {row.account_id}, Name: {row.account_type}')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
