from flask import render_template, request, redirect, url_for, make_response
import requests
from flask_login import login_user, logout_user
from app import app, db
from app.model.User import User
from ast import literal_eval
from sqlalchemy import func
from requests import api
from json import dumps, loads


@app.route('/loginApi', methods=['POST'])
def login():
    if request.method == 'POST':

        request_data = request.get_json()

        email = request_data['email']
        password = request_data['password']

        user = User.query.filter_by(email=email).first()

        if user is None:
            return literal_eval(str({"response": "Email informado inválido ou não existe."}))

        if not User or not user.verify_password(password):
            # return redirect(url_for('login'))
            return literal_eval(str({"response": "Senha inválida."}))

        # login_user(user)
        # return redirect(url_for('home'))
        return literal_eval(str({"response": user}))

    #     email = request.json['email']
    #     password = request.json['password']

    #     user = User.query.filter_by(email=email).first()

    #     if not User or not user.verify_password(password):
    #         return redirect(url_for('login'))

    #     login_user(user)
    #     return redirect(url_for('home'))

    # return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
