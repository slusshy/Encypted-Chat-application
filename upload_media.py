from firebase_admin import storage

bucket = storage.bucket()
blob = bucket.blob("media/user1/photo.jpg")
blob.upload_from_filename("local_photo.jpg")
blob.make_public()

# In send_message.py
def send_media_message(chat_id, sender_id, media_path):
    blob = bucket.blob(f"chats/{chat_id}/{media_path}")
    blob.upload_from_filename(media_path)
    public_url = blob.public_url
    send_message(chat_id, sender_id, f"MEDIA_URL:{public_url}")

print("Public URL:", blob.public_url)
