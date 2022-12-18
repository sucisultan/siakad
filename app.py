from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from db import db

from backend.auth import authapp
from backend.mahasiswa import mhsapp
from backend.jurusan import jurusanapp
from backend.absensi import absensiapp

app = Flask(__name__, static_folder='static',static_url_path='')

app.secret_key = '1n1r4h4s14'

app.register_blueprint(authapp)
app.register_blueprint(mhsapp)
app.register_blueprint(jurusanapp)
app.register_blueprint(absensiapp)

@app.route('/')
def index():
    return redirect(url_for('authapp.login'))

@app.route('/cek_session')
def cek_session():
    return jsonify(session['user'])



if __name__ == '__main__':
    app.run(debug=True)