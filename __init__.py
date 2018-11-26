# This file is used to initialize global variables
# Like the Flask app and database cursor
from flask import Flask
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('goshna.sqlite', check_same_thread=False)
c = conn.cursor()

# clear old data
# c.execute('''drop table if exists flights''')
# c.execute('''drop table if exists messages''')
# c.execute('''drop table if exists airlines''')
# c.execute('''drop table if exists airports''')
# c.execute('''drop table if exists users''')
# c.execute('''drop table if exists listening_users''')
# c.execute('''drop table if exists gates''')
# c.execute('''drop table if exists flight_gates''')

# Flights
# ! remove source airport
# ! merge date and time
c.execute('''create table if not exists flights(id integer primary key autoincrement, airline_id int, dest_airport text, flight_number int, gate text, departure int)''')

# Messages
# ! change text field to body
c.execute('''create table if not exists messages(id integer primary key autoincrement, body text, time int, flight_id int)''')

# Airlines
c.execute('''create table if not exists airlines(id integer primary key autoincrement, airline_short text, airline_full text)''')
c.execute('''insert into airlines (airline_short, airline_full) values ('Goshna', 'Goshna Airline')''')

# # Airports
# # ! removed
# # c.execute('''create table if not exists airports(id integer primary key autoincrement, airport_short text, airport_full text)''')

# Users
c.execute('''create table if not exists users(id integer primary key autoincrement)''')

# ListeningUsers
c.execute('''create table if not exists listening_users(user_id int, flight_id int)''')

# # Gates
# # ! removed
# # c.execute('''create table if not exists gates(id integer primary key autoincrement, name text, airport_id int)''')

# # FlightGates
# # ! removed
# # c.execute('''create table if not exists flight_gates(id integer primary key autoincrement, flight_id int, gate_id int)''')

conn.commit()
