from flask import Flask, jsonify, abort, request
from goshna import *
from goshna import ApiFunctions

class FlightID:
    def __init__(self, flight_id):
        self.flight_id = flight_id

    def to_json(self):
        return {'flight_id': self.flight_id}

class ListeningUser:
    def __init__(self, user_id, flight_id):
        self.user_id = user_id
        self.flight_id = flight_id

    def to_json(self):
        return {'user_id': self.user_id, 'flight_id': self.flight_id}

    @app.route('/goshna/api/listening_users', methods=['GET'])
    def get_listening_users():
        listening_users = []
        results = ApiFunctions.query_db("SELECT * FROM listening_users")
        for row in results:
            listening_user = ListeningUser(row['user_id'], row['flight_id'])
            listening_users.append(listening_user.to_json())

        return jsonify({'listening_users': listening_users})

    @app.route('/goshna/api/flights/adduser/<int:user_id>/<int:flight_id>', methods=['GET'])
    def add_listening_user(user_id, flight_id):
        
        result = ApiFunctions.post_db("INSERT INTO listening_users VALUES (?, ?)", [user_id, flight_id]);
        inserted_id = c.lastrowid
        print u'Inserted new listening_user at row ' + str(inserted_id)
        return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/flights/removeuser/<int:user_id>/<int:flight_id>', methods=['GET'])
    def remove_listening_user(user_id, flight_id):
        
        ApiFunctions.post_db("DELETE FROM listening_users WHERE user_id=? and flight_id=?", [user_id, flight_id])
        print u'Deleted listening_user with ID ' + str(0)
        return jsonify({'id': str(0)})

    @app.route('/goshna/api/users/getflights/<int:user_id>', methods=['GET'])
    def get_user_flights(user_id):
        flight_ids = []
        results = ApiFunctions.query_db("SELECT * FROM listening_users where user_id=?", [user_id])
        for row in results:
            flight_id = FlightID(row['flight_id'])
            flight_ids.append(flight_id.to_json())

        return jsonify({'flights': flight_ids})
