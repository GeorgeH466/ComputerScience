import bcrypt

def create_hash(password):#uses an inputted password to create a hash of the password
    password_bytes = password.encode()
    salt = bcrypt.gensalt()#adds a salt (random string of characters) to increase security
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode(), salt.decode()

def check_password(password, hashed):#checks a password entered to a stored hash value
    return bcrypt.checkpw(password.encode(), hashed.encode())

if __name__ == '__register__':
    create_hash()
elif __name__ == '__login__':
    check_password()