# import hashlib
from functions import hash_password, check_password, generate_salt
from connection import connect, connect1
import datetime
# import psycopg2

class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self._hashed_password = hash_password(password, salt)
        self.username = username

    #getter to read id and hashed_password
    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    #setter to chage password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    #methods must have cursor as argument

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = '''
        SELECT id, username, hashed_password FROM users WHERE username = %s
        '''
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user.username = username
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql ='''
        SELECT id, username, hashed_password FROM users
        WHERE id = %s
        '''
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = '''
        SELECT id, username, hashed_password FROM users
        '''
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hash_password
            users.append(loaded_user)
        return users


    def delete(self, cursor):
        sql = '''
        DELETE FROM users WHERE id=%s
        '''
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

class Messages:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def id(self):
        return self._id


    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date)
                             VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text, datetime.date.today())
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text = %s, creation_date=%s
                            WHERE id=%s"""
            values = (self.from_id, self.to_id, self.id, self.text, datetime.date.today())
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql = '''
        SELECT id, from_id, to_id, text FROM messages
        '''
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text = row
            loaded_message = Messages
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.text = text
            messages.append(loaded_message)
        return messages


if __name__ == "__main__":
    cursor = connect1().cursor()

    a = User.load_user_by_username(cursor, "Dodo")
    print(a[0])


    connect1().close()