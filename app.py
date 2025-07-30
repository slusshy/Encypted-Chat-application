import traceback
from flask import Flask, request, jsonify
from firebase_init import db
from datetime import datetime

app = Flask(__name__)

@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        print("=== Register user function called ===")
        data = request.get_json()
        print(f"Received data: {data}")
        
        username = data.get('username')
        password = data.get('password')
        
        if not (username and password):
            return jsonify({'status': 'fail', 'reason': 'Missing username or password'}), 400
        
        db.collection('users').document(username).set({
            'password': password
        })
        print("User registered successfully!")
        return jsonify({'status': 'success'})
    except Exception as e:
        print("=== REGISTER USER ERROR ===")
        traceback.print_exc()
        return jsonify({'status': 'error', 'reason': str(e)}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        print("=== Send message function called ===")
        
        # Check if request has JSON
        if not request.is_json:
            print("ERROR: Request is not JSON")
            return jsonify({'status': 'fail', 'reason': 'Request must be JSON'}), 400
        
        # Get data safely
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Check required fields
        chat_id = data.get('chat_id')
        sender = data.get('sender')
        message = data.get('message')
        
        print(f"chat_id={chat_id}, sender={sender}, message={message}")
        
        if not chat_id:
            print("ERROR: chat_id missing")
            return jsonify({'status': 'fail', 'reason': 'chat_id required'}), 400
            
        if not sender:
            print("ERROR: sender missing")
            return jsonify({'status': 'fail', 'reason': 'sender required'}), 400
            
        if not message:
            print("ERROR: message missing")
            return jsonify({'status': 'fail', 'reason': 'message required'}), 400
        
        print("All fields present, attempting Firestore write...")
        
        # Add document to Firestore
        db.collection('chats').document(chat_id).collection('messages').add({
            'sender': sender,
            'message': message,
            'timestamp': datetime.utcnow()
        })
        
        print("Message added to Firestore successfully!")
        return jsonify({'status': 'sent'})
        
    except Exception as e:
        print("=== SEND MESSAGE ERROR ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        traceback.print_exc()
        return jsonify({'status': 'error', 'reason': str(e)}), 500

@app.route('/fetch_messages', methods=['GET'])
def fetch_messages():
    try:
        print("=== Fetch messages function called ===")
        chat_id = request.args.get('chat_id')
        print(f"Fetching messages for chat_id: {chat_id}")
        
        if not chat_id:
            return jsonify([])
        
        msgs = db.collection('chats').document(chat_id).collection('messages').order_by("timestamp").stream()
        messages = []
        for m in msgs:
            d = m.to_dict()
            messages.append({
                'sender': d.get('sender'),
                'message': d.get('message'),
                'timestamp': str(d.get('timestamp'))
            })
        
        print(f"Found {len(messages)} messages")
        return jsonify(messages)
        
    except Exception as e:
        print("=== FETCH MESSAGES ERROR ===")
        traceback.print_exc()
        return jsonify({'status': 'error', 'reason': str(e)}), 500

@app.route('/')
def home():
    return "Server is running!"

if __name__ == '__main__':
    # ⚠️ THIS is the magic fix
    app.run(host='0.0.0.0', port=5000, debug=True)

