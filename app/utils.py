from passlib.context import CryptContext

pwdContext = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hashFunc(password: str):
    return pwdContext.hash(password)

def verifyPassword(plainPassword, hashPassword):
    return pwdContext.verify(plainPassword, hashPassword)