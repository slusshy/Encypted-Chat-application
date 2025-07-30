from firebase_init import db

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            msg = change.document.to_dict()
            print(f"New message from {msg['sender_id']}: {decrypt_msg(msg['encrypted_msg'])}")

# Start listener
db.collection("chats").document("group1").collection("messages").on_snapshot(on_snapshot)