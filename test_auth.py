from auth_service import create_user, get_user_by_email

# TEST CREATE
create_user("ayush123@gmail.com", "strongPass@123")

# TEST FETCH
get_user_by_email("ayush123@gmail.com")
