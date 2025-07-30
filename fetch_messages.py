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
            print(f"Document data: {d}")  # Debug: document ka data dekho
            messages.append({
                'sender': d.get('sender'),       # ✅ Yeh field sahi hai
                'message': d.get('message'),     # ✅ Yeh field sahi hai  
                'timestamp': str(d.get('timestamp'))
            })
        
        print(f"Found {len(messages)} messages")
        print(f"Messages data: {messages}")  # Debug: final messages dekho
        return jsonify(messages)
        
    except Exception as e:
        print("=== FETCH MESSAGES ERROR ===")
        traceback.print_exc()
        return jsonify({'status': 'error', 'reason': str(e)}), 500
