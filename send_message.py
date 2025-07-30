import traceback
from flask import Flask, request, jsonify
from firebase_init import db
from datetime import datetime

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        print("=== Send message function called ===")
        data = request.get_json()
        print(f"Received data: {data}")
        
        chat_id = data.get('chat_id')
        sender = data.get('sender_username')    # ✅ Change: 'sender' se 'sender_username'
        message = data.get('msg')               # ✅ Change: 'message' se 'msg'
        
        print(f"chat_id={chat_id}, sender={sender}, message={message}")
        
        if not chat_id:
            print("ERROR: chat_id missing")
            return jsonify({'status': 'fail', 'reason': 'chat_id required'}), 400
            
        if not sender:
            print("ERROR: sender_username missing")
            return jsonify({'status': 'fail', 'reason': 'sender_username required'}), 400
            
        if not message:
            print("ERROR: msg missing")
            return jsonify({'status': 'fail', 'reason': 'msg required'}), 400
        
        print("All fields present, attempting Firestore write...")
        
        # Firestore me save karo
        db.collection('chats').document(chat_id).collection('messages').add({
            'sender': sender,           # Field naam same rakho ya jaise chaaho
            'message': message,         # Field naam same rakho ya jaise chaaho  
            'timestamp': datetime.utcnow()
        })
        
        print("Message added to Firestore successfully!")
        return jsonify({'status': 'sent'})
        
    except Exception as e:
        print("=== SEND MESSAGE ERROR ===")
        traceback.print_exc()
        return jsonify({'status': 'error', 'reason': str(e)}), 500
