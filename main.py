from login import take_username #take_username initiates the login process

def main():
    print("Welcome, please log in!") #welcome message
    take_username() #call login functions
    
if __name__ == "__main__":
    main() #trigger main variable if name of the file being used is "main"