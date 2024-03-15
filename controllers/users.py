from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connector import Session
from sqlalchemy.orm import sessionmaker
from connectors.mysql_connector import engine
from models.user import User
from cerberus import Validator
from validations.user_schema import user_schema

from flask_login import current_user, login_required



users_route = Blueprint('users_route',__name__)

@users_route.route("/users", methods=['GET'])
@login_required
# @jwt_required
def get_users():

    try:
        print(current_user.user_id)
        print(current_user)
        if not current_user.is_authenticated:
            return jsonify({"error": "User not authenticated"}), 401

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        users = session.query(User).all()
        user_data = [{"user_id": user.user_id, "username": user.username, "email": user.email} for user in users]
        session.close()

        return jsonify({"users": user_data}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Error processing data"}), 500


@users_route.route("/users/<int:user_id>", methods=['GET'])
@login_required
# @jwt_required
def get_user_id(user_id):

    try:

        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()

        if not current_user.is_authenticated:
            return jsonify({"error": "User not authenticated"}), 401
        
        session = Session()
        user = session.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        return jsonify({"user": user.serialize()})
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": "Error Processing Data"}), 500
    finally:
        session.close()
    

@users_route.route("/users/<int:user_id>", methods=['PUT'])
@login_required
# @jwt_required
def product_update(user_id):

    v = Validator(user_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    user = session.query(User).filter(User.user_id== user_id).first()
    try:

        user.username = json_data['username']
        user.email = json_data['email']
        user.set_password(json_data['password'])

        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        return { "message": "Fail to Update data"}
    
    return { "message": "Success updating data"}

@users_route.route("/users/<int:id>", methods=['DELETE'])
@login_required
# @jwt_required
# @role_required('DIRECTOR', 'Admin')
def product_delete(id):

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()


    try:
        session.begin()

        user = session.query(User).filter(User.id==id).first()
        
        if user:
            session.delete(user)
            session.commit()
            return { "message": "Success delete data"}
        else:
            return {"message": "USER not found"}
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": f"Fail to delete data: {str(e)}"}
    finally:
        session.close()




