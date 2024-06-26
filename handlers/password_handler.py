import bcrypt
import sys
from mysql.connector import Error


def authenticate_user(username, password, db):
    userTable = "users"
    itemToFind = "hashed_password"

    #check and see if username exists in database need to set up interface!!!
    if does_user_exist(username, userTable, db) is False:
        return False

    #hashed_password will need to be retrieved from database where given username matches the username in table.
    hashed_password = get_record_item(username, itemToFind, userTable, db).encode('utf-8')

    #This hashes the given password then compares hashed password that is stored.
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False


def does_user_exist(username, table,  db):
    with db.cursor() as cursor:

        query = f'SELECT * FROM {table} WHERE username = %s'

        cursor.execute(query, (username,))

        record = cursor.fetchone()

        if record:
            return True
        else:
            return False


def get_record_item(username, item, table, db):
    with db.cursor() as cursor:

        query = f'SELECT {item} FROM {table} WHERE username = %s'

        cursor.execute(query, (username,))

        record = cursor.fetchone()

        (give_item,) = record

        return give_item

def store_password(username, hashed_password, db):
    with db.cursor() as cursor:
        query = "INSERT INTO users (username, hashed_password) VALUES (%s, %s)"

        cursor.execute(query, (username, hashed_password))

        db.commit()
    return


def update_password(username, hashed_password, db):
    with db.cursor() as cursor:
        query = "UPDATE users SET hashed_password = %s WHERE username = %s"

        cursor.execute(query, (hashed_password, username))

        db.commit()
    return

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def check_user_pass_validity(password):
    if " " in password:
        return False
    passlength = len(password)
    if passlength <= 7 or passlength > 16:
        return False
    if not password.isascii():
        return False
    return True






