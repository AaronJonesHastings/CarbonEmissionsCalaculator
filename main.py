#open login page

from login import verify_password
login_attempts = 0 #locks account when login_attempts = 3
username = input("Please enter your username:\n")
verify_password(username, login_attempts)