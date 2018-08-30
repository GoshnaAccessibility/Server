from flask import Flask, jsonify, abort, request
from goshna import *
from goshna import ApiFunctions

class Airline:
    def __init__(self, id, airline_short, airline_full):
        self.id = id
        self.airline_short = airline_short
        self.airline_full = airline_full

    def to_json(self):
        return {
            'id': self.id, 
            'airline_short': self.airline_short, 
            'airline_full': self.airline_full
        }

    @app.route('/goshna/api/airlines', methods=['GET'])
    def get_airlines():
        airlines = []
        results = ApiFunctions.query_db("SELECT * FROM airlines")
        for row in results:
            airline = Airline(row['id'], row['airline_short'], row['airline_full'])
            airlines.append(airline.to_json())

        return jsonify({'airlines': airlines})

    @app.route('/goshna/api/airlines/<int:airline_id>', methods=['GET'])
    def get_airline(airline_id):

        row = ApiFunctions.query_db("SELECT * FROM airlines WHERE id = ?", [airline_id], one=True)
        if row is None:
            abort(404)

        airline = Airline(row['id'], row['airline_short'], row['airline_full'])
        return jsonify({'airline': airline.to_json()})

    @app.route('/goshna/api/airlines', methods=['POST'])
    def create_airline():
        if not request.json or not 'airline_short' in request.json or not 'airline_full' in request.json:
            abort(400)
        
        airline_short = request.json['airline_short']
        airline_full = request.json['airline_full']

        result = ApiFunctions.post_db("INSERT INTO airlines VALUES (NULL, ?, ?)", [airline_short, airline_full]);
        inserted_id = c.lastrowid

        print u'Inserted new airline at row ' + str(inserted_id)
        return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/airlines/<int:airline_id>', methods=['DELETE'])
    def delete_airline(airline_id):

        ApiFunctions.post_db("DELETE FROM airlines WHERE id=?", [airline_id])
        print u'Deleted airline with ID ' + str(inserted_id)
        return jsonify({'result': True})

