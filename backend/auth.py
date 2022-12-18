from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

authapp = Blueprint('authapp', __name__)


from functools import wraps

# diimport ke mahasiswa.py
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('authapp.login'))
    return wrapper

@authapp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
    # ambil data dari form
        data = {
            'username': request.form['username']

        }
        
    # lakukan pengecekan user
        user = {}
        user_ref = db.collection('users').where('username', '==', data['username']).stream()
        for ur in user_ref:
            user = ur.to_dict()
            
        if user:
            if check_password_hash(user['password'], request.form['password']):
                session['user'] = user
                flash('Berhasil Login', 'success')
                return redirect(url_for('mhsapp.mahasiswa'))
        
        flash('Username / Password salah', 'danger')
        return redirect(url_for('authapp.login'))
    # cek password
    # flash return
    if 'user' in session:
        return redirect(url_for('mhsapp.mahasiswa'))
    return render_template('login.html')

@authapp.route('/logout')
def logout():
    session.clear()
    flash('Anda Keluar', 'danger')
    return redirect(url_for('authapp.login'))

@authapp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        # mengambil form
        data = {
            'username': request.form['username'],
            'role': 'admin',
            'nama_lengkap': request.form['nama_lengkap'],
        }
        # cek password dan password_1
        if request.form['password'] != request.form['password_1']:
            flash('Password Tidak Sama', 'danger')
            return redirect(url_for('authapp.register'))
        
        if len(request.form['password']) <= 3:
            flash('Password harus lebih dari 3 kata', 'danger')
            return redirect(url_for('authapp.register'))
        
        data['password'] = generate_password_hash(request.form['password'], 'sha256')
        # cek username
        user = {}
        user_ref = db.collection('users').where('username', '==', data['username']).stream()
        for ur in user_ref:
            user = ur.to_dict()
            
        if user:
            flash('Username Sudah Ada', 'danger')
            return redirect(url_for('authapp.register'))
        # masukkan ke database
        db.collection('users').document().set(data)
        # flash
        flash('Berhasil Register', 'success')
        # return to login
        return redirect(url_for('authapp.login'))
    return render_template('register.html')