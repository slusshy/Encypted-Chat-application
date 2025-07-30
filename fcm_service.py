from firebase_admin import messaging

# ✅ Replace with actual token (from mobile app/console)
FCM_TOKEN = "I/flutter (12345): FCM Token: cKdP5m9... [Copy this]"  # e.g. "cKdP5m9...YOUR_TOKEN"

message = messaging.Message(
    notification=messaging.Notification(
        title="New Message",
        body="You've got a message!"
    ),
    token=FCM_TOKEN  # Use real token here
)

try:
    response = messaging.send(message)
    print('Successfully sent message:', response)
except Exception as e:
    print('🚨 FCM Error:', e)