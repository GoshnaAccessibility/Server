#!flask/bin/python
from flask import Flask
from Server import *
import Airport, Airline, Message, Flight, User, ListeningUser, Gate, FlightGate, DisplayFlight

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
