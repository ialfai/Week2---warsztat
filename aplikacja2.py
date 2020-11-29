import argparse
from models import User, Messages
from connection import connect1
from functions import hash_password, check_password


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="receiver of your message", action="store_true")
parser.add_argument("-s", "--send", help="content of a message")
parser.add_argument("-l", "--list", help="list users", action="store_true")

args = parser.parse_args()


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
            a = User.load_user_by_id(connect1().cursor(), to_id)
            if a != None:
                if len(text) < 255:
                    from_id = user1.id
                    message1 = Messages(from_id, to_id, text)
                    message1.save_to_db(connect1().cursor())
                    return "Message sent"
                else:
                    print('Your message is too long, should be maximum 255 characters')
            else:
                print("Receiver\'s id is incorrect")
        else:
            print('Wrong password')


if __name__ == "__main__":
    if args.password and args.username and args.list:
        list_all_messages(args.username, args.password)
    elif args.username and args.password and args.to and args.send:
        send_a_massage(args.username, args.password, args.to, args.send)
    else:
        parser.print_help()



