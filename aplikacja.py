import argparse
from models import User, Messages
from connection import connect1
from functions import hash_password, check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit", action="store_true")

args = parser.parse_args()


def create_user(username, password):
    if len(password) < 8:
        print('password is too short')
    elif User.load_user_by_username(connect1().cursor(), username) != None:
        print('This username already exists, choose a different one')
    else:
        a = User(username, password)
        cursor = connect1().cursor()
        a.save_to_db(cursor)
        connect1().close()
        return "User created"

def change_password(username, password, new_pass):
    if User.load_user_by_username(connect1().cursor(), username) == None:
        print('This username doesn\'t exists, submit a correct username')
    else:
        user1 = User.load_user_by_username(connect1().cursor(), username)
        if check_password(str(password), user1.hashed_password):
            if len(new_pass) < 8:
                print('Password should have minimum 8 characters')
            else:
                user1.hashed_password = hash_password(new_pass, 'salt')
                user1.save_to_db(connect1().cursor())
                connect1().close()
                return "New password has been set"
        else:
            print('The submitted password is incorrect')



def delete_user(username, password):
    if User.load_user_by_username(connect1().cursor(), username) == None:
        print('This username doesn\'t exists, submit a correct username')
    else:
        user1 = User.load_user_by_username(connect1().cursor(), username)
        if check_password(str(password), user1.hashed_password):
            user1.delete(connect1().cursor())
            connect1().close()
            return f"User {username} has been successfully removed"
        else:
            print('The submitted password is incorrect')


def list_all_users():
    user1 = User.load_all_users(connect1().cursor())
    for i in user1:
        print(i.username)

def list_all_messages(username, password):
    if User.load_user_by_username(connect1().cursor(), username) == None:
        print('This username doesn\'t exists, submit a correct username')
    else:
        user1 = User.load_user_by_username(connect1().cursor(), username)
        if check_password(str(password), user1.hashed_password):
            messages = user1.load_messages_by_user_id(connect1().cursor())
            return messages
        else:
            print('The submitted password is incorrect')



def send_a_massage(username, password, to_id, text):
    if User.load_user_by_username(connect1().cursor(), username) == None:
        print('This username doesn\'t exists, submit a correct username')
    else:
        user1 = User.load_user_by_username(connect1().cursor(), username)
        if check_password(str(password), user1.hashed_password):
            from_id = user1.id
            message1 = Messages(from_id, to_id, text)
            message1.save_to_db(connect1().cursor())
            return "Message sent"













# if __name__ == "__main__":
    if args.password and args.username:
        create_user(args.username, args.password)
    elif args.username and args.password and args.edit and args.new_pass:
        change_password(args.username, args.password, args.new_password)
    elif args.username and args.password and args.delete:
        delete_user(args.username, args.password)
    elif args.list:
        list_all_users()
    else:
        parser.print_help()


if __name__ == "__main__":

    # create_user("Baba", 'Beirut123')
    # a = User.load_user_by_username(connect1().cursor() ,"Baba")
    # print(a.id)
    # b = list_all_messages("Baba", "Beirut123")
    # for i in b:
    #     print(i.creation_date)