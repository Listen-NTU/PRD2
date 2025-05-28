from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route('/api/message', methods=['POST'])
def add_message():
    data = request.json
    db.collection('messages').add({
        'userId': data['userId'],
        'content': data['content']
    })
    return jsonify({'status': 'success'})

@app.route('/api/messages', methods=['GET'])
def get_messages():
    docs = db.collection('messages').stream()
    result = []
    for doc in docs:
        msg = doc.to_dict()
        msg['id'] = doc.id
        result.append(msg)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

