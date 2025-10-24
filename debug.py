from utils.security import create_access_token,verify_access_token
t = create_access_token("sunday@gmail.com")
print("msg:", t)
print("verity:", verify_access_token(t))