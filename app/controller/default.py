from flask import render_template, request, redirect, url_for, make_response
import requests
from flask_login import login_user, logout_user
from app import app, db
from app.model.User import User, AlchemyEncoder
from ast import literal_eval
from sqlalchemy import func
from requests import api
from json import dumps, loads


@app.route('/loginApi/<email>/<password>', methods=['POST'])
def login(email, password):
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()

        if user is None:
            return '{"response": "Email informado inválido ou não existe."}'

        if not User or not user.verify_password(password):
            return '{"response": "Senha inválida."}'

        return dumps({"response": user.id})


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
