import hashlib
from functions import hash_password, check_password, generate_salt
from connection import connect, connect1

class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self._hashed_password = hash_password(password, salt)
        self.username = username

    #getter to read id and hashed_password
    @property
    def id(self):
        return self.id

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
            sql = '''
            INSERT INTO users(username, hashed_password)
            values(%s, %s) RETURNING id
            '''
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        return False
    #
    # def load_user_by_username(self):
    #     return
    #
    # def load_user_by_id(self):
    #     return
    #
    # def load_all_users(self):
    #     return
    #
    # def delete(self):
    #     return

if __name__ == "__main__":
    cursor = connect1().cursor()
    user1 = User("Dodo", "mocnehaslo")

    user1.save_to_db(cursor)
    connect1().close()

