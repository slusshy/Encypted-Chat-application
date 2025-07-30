import sys
sys.path.append(r"D:\Backend")  # Raw string to handle backslashes
from send_message import send_message

# Raw message bhejo (encryption automatically hoga)
send_message("Aayush_Y", "ayush_uid_123", "Hello Bhai!")  # No need for "ENCRYPTED:" prefix