import dbConnection #imports the database details
import bcrypt
global login_attempts
from user_direct_class import direction_picklist #library used for decryption

#get user details at login

username = input("Please enter your username: ")

login_attempts = 0 #locks account when login_attempts = 3

def generate_session_id():
    import uuid
    return str(uuid.uuid4())

#define the variable to verify the password
def verify_password(username, login_attempts):
    login_attempts = 0
    password = input("Please enter your password: ")
    cursor = dbConnection.db.cursor()
    exists_check = "SELECT username FROM user_details WHERE username = %s"
    val = (username,)
    cursor.execute(exists_check, val)
    result = cursor.fetchone()
    if result:
        lockout = 0
        locked_query = "SELECT locked FROM user_details WHERE username = %s"
        val = (username,)
        cursor.execute(locked_query, val)
        locked = cursor.fetchone()
        print(locked)
        if locked == (0,):
            if login_attempts < 3:
                #username = input("Please enter your username")
                #password = input("Please enter your password")
                sql = "SELECT password FROM user_details WHERE username = %s" #SQL query to pass
                cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
                cursor.execute(sql, (username,)) #execute the SQL. Passing named parameters for safety (SQL injections)
                result = cursor.fetchone() #store restult in variable

                if result:
                    stored_hash = result[0].encode('utf-8') #get hash in bytes
                    #now verify the password against the stored hash
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        print("Password Accepted")
                        from user_direct_class import direction_picklist
                        direction_picklist.page_direction(username)
                        return True #decrypt successful
                    else:
                        print("Password Not Accepted")
                        login_attempts = login_attempts + 1
                        print(f"New login attempts value = {login_attempts}")
                        return verify_password(username, login_attempts) #decrpyt failed
                else:
                    print("User Not Found")
                    return False #no match in user_details table
            else:
                import userClass
                userClass.user.lockout(username)
                #lockout = 1
                #sql = "UPDATE user_details SET locked = %s WHERE username = %s"
                #val = (lockout, username,)
                #cursor.execute(sql, val)
                #dbConnection.db.commit()
                #print("Your account is locked, please contact support or use the forgotten password function")
        else:
            print("Your account is locked, please contact support or use the forgotten password function")
    else:
        import inquirer
        #determine if user's average should be used for the day's emission calculation
        create_question = [
            inquirer.List ('create_account',
                           message = "User does not exists, would you like to create an account?",
                           choices = [ "Yes", "No"],
            ),
        ]

        create_answer = inquirer.prompt(create_question)
    
        choice = (create_answer['create_account'])
        if choice == "Yes":
            from userSignUp import userSignUp
            userSignUp()
        else:
            exit

verify_password(username, login_attempts)
