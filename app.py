#!flask/bin/python
from Server import *
import Airport, Airline, Message, Flight, User, ListeningUser, Gate, FlightGate, DisplayFlight

if __name__ == '__main__':
    print("II - Launching the Flask server")
    app.run(host='0.0.0.0', threaded=True, debug=True)
