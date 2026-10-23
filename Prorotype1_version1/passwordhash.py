import bcrypt

def create_hash():
    password = b"testing123"
    salt = bcrypt.gensalt()
    store_salt=str(salt)
    hashed = bcrypt.hashpw(password, salt)
    print(store_salt)
    entered = b"testing123"
def check_password(entered, hashed):
    if bcrypt.checkpw(entered, hashed):
        print("Password correct")
        print(hashed)
    else:
        print("Wrong password")

if __name__ == "__main__":
    create_hash()
    check_password()