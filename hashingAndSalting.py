import bcrypt

def hash_password(password):
    """
    hashes a password with a generated salt using the 
    bcrypt library
    
    Args:
    password (str) used as the password to hash
    
    Returns:
    bytes - the hashed password with salt
    """
    
    #Generate the salt
    salt = bcrypt.gensalt()
    #now hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    #print(hashed_password)
    return hashed_password

password = "d4urVmrq1!"
#hash_password(password)


def verify_password(stored_hash, password):
    """
    Verifies a password against a stored hash.
    
    Args:
        stored_hash (bytes): The stored hashed password.
        password (str): The password to verify.
        
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

stored_hash = hash_password("d4urVmrq1!")
print(verify_password(stored_hash, "d4urVmrq1!"))  # Should return True