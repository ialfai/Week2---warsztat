import argparse
from models import User
from connection import connect, connect1
from functions import hash_password, generate_salt, check_password, list_all_users, delete_user, change_password, create_user


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit", action="store_true")

args = parser.parse_args()


def aplikacja():
        if args.password and args.username:
            create_user(args.username, args.password)
        elif args.username and args.password and args.edit and args.new_pass:
            change_password(args.username, args.password, args.new_password)
        elif args.username and args.password and args.delete:
            delete_user(args.username, args.password)
        elif args.list:
            list_all_users()
        else:
            return parser.print_help()





if __name__ == "__main__":
    # create_user('Lola', 'haseleczko')

    # aaaaaaaaaaaaaaaaaacac24793313207d1628bcc4f4931cf8c64620df388e48f653f071e38d9d2f7
    # aaaaaaaaaaaaaaaaaacac24793313207d1628bcc4f4931cf8c64620df388e48f653f071e38d9d2f7
    # user1 = User.load_user_by_username(connect1().cursor(), "Mamba")

    # delete_user("Lola", 'haseleczko')
    # print(check_password("dobrehaslo", ''))
    # b = list_all_users()
    # for i in b:
    #     print(i.username)