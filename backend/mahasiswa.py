from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from db import db, get_all_collection, storage
from backend.auth import login_required
mhsapp = Blueprint('mhsapp', __name__)

@mhsapp.route('/mahasiswa')
@login_required
def mahasiswa():
    daftar_mahasiswa = []
    # memanggil semua data di collection mahasiswa
    mahasiswa_ref = db.collection('mahasiswa').stream()
    # melakukan looping
    for mr in mahasiswa_ref:
        mhs = mr.to_dict()
        mhs['id'] = mr.id
        
    # append ke dalam daftar mahasiswa
        daftar_mahasiswa.append(mhs)
    return render_template('mahasiswa.html', data=daftar_mahasiswa)

# Menghapus Mahasiswa
@mhsapp.route('/mahasiswa/delete/', methods=['POST'])
@login_required
def delete_mahasiswa():
    if request.method == 'POST':
        uid = request.form.get('uid')

        db.collection('mahasiswa').document(uid).delete()
        flash('Mahasiswa Telah Dihapus', 'danger')
        return('', 204)
# Selesai menghapus Mahasiswa


@mhsapp.route('/mahasiswa/<uid>')
@login_required
def lihat_mahasiswa(uid):
    # mendapatkan data berdasarkan id
    mhs = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('lihat_mahasiswa.html', data=mhs)

@mhsapp.route('/mahasiswa/tambah', methods=['POST', 'GET'])
@login_required
def tambah_mahasiswa():
    if request.method == 'POST':
        # mengambil data dari front end
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'nim': request.form['nim'],
            'tgl_lahir': request.form['tgl_lahir'],
            'email': request.form['email'],
            'jurusan': request.form['jurusan'],
            'role': 'mahasiswa',
            'is_active': True
        }
        # menambahkan foto
        if 'foto' in request.files and request.files['foto']:
            image = request.files['foto']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"profil/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['foto'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.tambah_mahasiswa'))
        # selesai menambahkan foto
        # menyimpan ke database
        # create
        db.collection('mahasiswa').document().set(data)
        # kembali ke halaman mahasiswa
        flash('Berhasil Menambahkan Mahasiswa', 'success')
        return redirect(url_for('.mahasiswa'))
    # membuat ada pilihan (forms) di jurusan mhs
    jurusan = get_all_collection('jurusan')
    return render_template('tambah_mahasiswa.html', jurusan=jurusan)
    


@mhsapp.route('/mahasiswa/edit/<uid>', methods=['POST', 'GET'])
@login_required
def edit_mahasiswa(uid):
    if request.method == 'POST':
        # menyimpan ke dalam variable data
        # update data
        # kembali ke halaman mahasiswa
        return "oke"
    mhs = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('edit_mahasiswa.html', data=mhs)