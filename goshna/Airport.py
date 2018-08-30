from flask import Flask, jsonify, abort, request
from goshna import *
from goshna import ApiFunctions

class Airport:
    def __init__(self, id, airport_short, airport_full):
        self.id = id
        self.airport_short = airport_short
        self.airport_full = airport_full

    def to_json(self):
        return {
			'id': self.id, 
			'airport_short': self.airport_short, 
			'airport_full': self.airport_full
		}

    @app.route('/goshna/api/airports', methods=['GET'])
    def get_airports():
        airports = []
        results = ApiFunctions.query_db("SELECT * FROM airports")
        for row in results:
            airport = Airport(row['id'], row['airport_short'], row['airport_full'])
            airports.append(airport.to_json())

        return jsonify({'airports': airports})

    @app.route('/goshna/api/airports/<int:airport_id>', methods=['GET'])
    def get_airport(airport_id):

        row = ApiFunctions.query_db("SELECT * FROM airports WHERE id = ?", [airport_id], one=True)
        if row is None:
            abort(404)

        airport = Airport(row['id'], row['airport_short'], row['airport_full'])
        return jsonify({'airport': airport.to_json()})

    @app.route('/goshna/api/airports', methods=['POST'])
    def create_airport():
        if not request.json or not 'airport_short' in request.json or not 'airport_full' in request.json:
            abort(400)
        
        airport_short = request.json['airport_short']
        airport_full = request.json['airport_full']

        result = ApiFunctions.post_db("INSERT INTO airports VALUES (NULL, ?, ?)", [airport_short, airport_full]);
        inserted_id = c.lastrowid

        print u'Inserted new airport at row ' + str(inserted_id)
        return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/airports/<int:airport_id>', methods=['DELETE'])
    def delete_airport(airport_id):

        ApiFunctions.post_db("DELETE FROM airports WHERE id=?", [airport_id])
        print u'Deleted airport with ID ' + str(inserted_id)
        return jsonify({'result': True})

