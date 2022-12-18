import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

firebaseConfig = {
    "apiKey": "AIzaSyDm4SDwnD4jpUEBrfXrHHrtwLWRN-OIC14",
    "authDomain": "siakaddatabase.firebaseapp.com",
    "databaseURL": "https://siakaddatabase-default-rtdb.firebaseio.com",
    "projectId": "siakaddatabase",
    "storageBucket": "siakaddatabase.appspot.com",
    "messagingSenderId": "173783424868",
    "appId": "1:173783424868:web:b66512a87b3dad6ba26471"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN