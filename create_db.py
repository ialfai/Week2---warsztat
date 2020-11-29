# Connection

from functions import execute_query
from connection import connect, connect1

# Database

query ='''CREATE DATABASE aplikacja;'''

try:
    execute_query(query, False, connect())
except Exception:
    print("taka baza danych już istnieje")

#connecting to aplikacja database

connect1()

# Users and messages tables


query_users_table = '''
    CREATE TABLE users(
    id serial primary key,
    username varchar(255),
    hashed_password varchar(80)
    )
'''

query_messages_table = '''
    CREATE TABLE messages(
    id serial primary key,
    from_id int,
    to_id int, 
    text varchar (300),
    creation_date timestamp,
    foreign key (from_id) references users(id),
    foreign key (to_id) references users(id)
    )
'''

try:
    execute_query(query_users_table, False)
except Exception:
    print("taka tabela już istnieje")

try:
    execute_query(query_messages_table, False)
except Exception:
    print("taka tabela już istnieje")

