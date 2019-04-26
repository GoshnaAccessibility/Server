# This file is used to initialize global variables
# Like the Flask app and database cursor
from ConfigParser import ConfigParser  # Python2
# from configparser import ConfigParser  # Python3
from flask import Flask
import os


def config(filename='database.ini', section='postgresql'):
    """
    Reads a configuration file for DB connection parameters.

    Sourced: http://www.postgresqltutorial.com/postgresql-python/connect/
    """
    # Check file exists
    if not os.path.isfile(filename):
        # file does not exist
        raise Exception('WW - DB Config file does not exist: {0}'
                        .format(filename))
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(('WW - DB Config - Section {0} not found in the {1} '
                         'file').format(section, filename))
    return db


app = Flask(__name__)

# DB connection
conn = None
create_table_flights = None
# Default DB queries
create_table_flights = ('create table if not exists flights(id integer primary'
                        ' key autoincrement, airline_id int, dest_airport '
                        'text, flight_number int, gate text, departure int)')
create_table_messages = ('create table if not exists messages(id integer '
                         'primary key autoincrement, body text, time int, '
                         'flight_id int)')
create_table_airlines = ('create table if not exists airlines(id integer '
                         'primary key autoincrement, airline_short text, '
                         'airline_full text)')
# create_table_airports = ('create table if not exists airports(id integer '
#                          'primary key autoincrement, airport_short text, '
#                          'airport_full text)')
create_table_users = ('create table if not exists users(id integer primary '
                      'key autoincrement)')
create_table_listening_users = ('create table if not exists listening_users('
                                'user_id int, flight_id int)')
# create_table_gates = ('create table if not exists gates(id integer primary '
#                       'key autoincrement, name text, airport_id int)')
# create_table_flight_gates = ('create table if not exists flight_gates(id '
#                              'integer primary key autoincrement, flight_id '
#                              'int, gate_id int)')
replace_airlines_goshna = ('replace into airlines values (1, "GO", '
                           '"Goshna Airlines")')
try:
    # read connection parameters
    params = config(filename='database-connection.ini', section='postgresql')

    # connect to the PostgreSQL server
    print('II - DB: connecting to the PostgreSQL database...')
    # Override SQL statements for PostgreSQL-specific syntax
    # E.g. autoincrement does not exist for psql, instead use 'serial' instead
    # of 'int' and remove keyword 'autoincrement':
    # https://www.tutorialspoint.com/postgresql/postgresql_using_autoincrement.htm
    create_table_flights = ('create table if not exists flights(id serial '
                            'primary key, airline_id int, dest_airport text, '
                            'flight_number int, gate text, departure int)')
    create_table_messages = ('create table if not exists messages(id serial '
                             'primary key, body text, time int, flight_id '
                             'int)')
    create_table_airlines = ('create table if not exists airlines(id serial '
                             'primary key, airline_short text, airline_full '
                             'text)')
    # create_table_airports = ('create table if not exists airports(id serial '
    #                          'primary key, airport_short text, airport_full '
    #                          'text)')
    create_table_users = ('create table if not exists users(id serial primary '
                          'key)')
    # create_table_gates = ('create table if not exists gates(id serial '
    #                       'primary key, name text, airport_id int)')
    # create_table_flight_gates = ('create table if not exists flight_gates('
    #                              'id serial primary key, flight_id int, '
    #                              'gate_id int)')
    replace_airlines_goshna = ('INSERT INTO airlines (id, airline_short, '
                               'airline_full) VALUES (1, \'GO\', \'Goshna '
                               'Airlines\') ON CONFLICT (id) DO UPDATE SET '
                               'airline_short = excluded.airline_short, '
                               'airline_full = excluded.airline_full')
    # Import the PostgreSQL module now (avoid deployment/debugging issues
    # on systems that do not have PostgreSQL server installed/running,
    # e.g. they are running on SQLite)
    import psycopg2  # PostgreSQL
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
except Exception as error:
    print(error)
    print("WW - Falling back to SQLite DB")
    import sqlite3  # Only import if necessary
    conn = sqlite3.connect('goshna.sqlite', check_same_thread=False)
c = conn.cursor()
print("II - DB: connected")

# clear old data
# c.execute('drop table if exists flights')
# c.execute('drop table if exists messages')
# c.execute('drop table if exists airlines')
# c.execute('drop table if exists airports')
# c.execute('drop table if exists users')
# c.execute('drop table if exists listening_users')
# c.execute('drop table if exists gates')
# c.execute('drop table if exists flight_gates')

# Flights
# ! remove source airport
# ! merge date and time
c.execute(create_table_flights)

# Messages
# ! change text field to body
c.execute(create_table_messages)

# Airlines
c.execute(create_table_airlines)
c.execute(replace_airlines_goshna)

# # Airports
# # ! removed
# c.execute(create_table_airports)

# Users
c.execute(create_table_users)

# ListeningUsers
c.execute(create_table_listening_users)

# # Gates
# # ! removed
# c.execute(create_table_gates)

# # FlightGates
# # ! removed
# c.execute(create_table_flight_gates)

conn.commit()
print("II - DB: ready")
