import hashlib

db = dict()

def register(username, password):
    db[username] = calc_md5(password+username+'the-Salt')

def calc_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

def authenticate(user, password):
    db_passwd = db.get(user)
    if db_passwd == calc_md5(password+user+'the-Salt'):
        print('True')
        return True
    else:
        print('False')
        return False

register('Andy','8800956')
print(db)
authenticate('Andy','8800956')






