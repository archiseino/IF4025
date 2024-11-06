from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("pc-cpu-monitoring-firebase-adminsdk-2yfd5-cf147c47f5.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pc-cpu-monitoring-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Referensi ke node 'cpu_usage' di Firebase
ref = db.reference('cpu_usage') 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/graph')
def index():
    return render_template('index.html')

## Getting the last currently updated snapshot data
## And put it in the List Comprehension before sending the Json data to App.py 
@app.route('/data')
def get_data():
    snapshot = ref.order_by_key().limit_to_last(10).get()   
    data = [{'cpu': value['cpu'], "disk": value["disk"], "net": value["net"], 'timestamp': value['timestamp']} for _, value in snapshot.items()]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)