from flask import Blueprint, json, jsonify, url_for, current_app, request, render_template
from API.model import *
from API.settings import App_name
from API.email_sender import *
import json
import random
from itsdangerous import URLSafeTimedSerializer
from API import mail, Message

app = current_app

members_bp = Blueprint("members_bp", __name__, template_folder='templates', static_folder='static')

@members_bp.route('/', methods=['POST','GET'])
def home():
    
    return "welcome members"
    

@members_bp.route('/register', methods=['POST','GET'])
def register():
    
    data = request.form
    name = data['name']
    address = data['address']
    email = data['email']
    phone = data['phone']
    password = data['password']

    # Check if user with the provided SCN number or email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with the email already exists'}), 409

    # Create a new user
    new_user = User(name, email, phone, address)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Generate verification code
    verification_code = generate_verification_code()  # You'll need to implement this function
    new_user.set_verification_code(str(verification_code))
    db.session.add(new_user)
    db.session.commit()

    # Send verification email
    send_verification_email(email, verification_code)  # You'll need to implement this function


    return jsonify({'message': 'User created successfully'}), 201





