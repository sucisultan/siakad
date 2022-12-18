from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from db import db
from backend.auth import login_required

jurusanapp = Blueprint('jurusanapp', __name__)

# Menambahkan jurusan/////////////
@jurusanapp.route('/jurusan', methods=['POST', 'GET'])
@login_required
def jurusan():
    if request.method == 'POST':
        # mengambil data dari front end
        data = {
            'jurusan': request.form['jurusan']
        }
    # menyimpan ke database
        # create
        db.collection('jurusan').document().set(data)
        # kembali ke halaman jurusan
        flash('Berhasil Menambahkan Jurusan', 'success')
        return redirect(url_for('.jurusan'))

    # memanggil semua data di collection jurusan
    # jurusan ref = nama variabelnya 
    # ref adalah referensi
    jurusan_ref = db.collection('jurusan').stream()
    data = []
    # melakukan looping
    # jr adalah jurusan ref
    for jr in jurusan_ref:
        use= jr.to_dict()
        use['id'] = jr.id
        data.append(use)
    return render_template('jurusan/jurusan.html', data=data)
# Selesai Menambahkan jurusan/////////////


# Menghapus Jurusan
@jurusanapp.route('/jurusan/delete/', methods=['POST'])
@login_required
def delete_jurusan():
    if request.method == 'POST':
        uid = request.form.get('uid')

        db.collection('jurusan').document(uid).delete()
        flash('Jurusan Telah Dihapus', 'danger')
        return('', 204)
# Selesai menghapus jurusan