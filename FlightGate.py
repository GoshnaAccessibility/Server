from flask import Flask, jsonify, abort, request
from goshna import *
from goshna import ApiFunctions

class FlightGate:
    def __init__(self, id, gate_id, flight_id):
        self.id = id
        self.gate_id = gate_id
        self.flight_id = flight_id

    def to_json(self):
		return {'id': self.id, 'gate_id': self.gate_id, 'flight_id': self.flight_id}

    @app.route('/goshna/api/flight_gates', methods=['GET'])
    def get_flight_gates():
        flight_gates = []
        results = ApiFunctions.query_db("SELECT * FROM flight_gates")
        for row in results:
            flight_gate = FlightGate(row['id'], row['gate_id'], row['flight_id'])
            flight_gates.append(flight_gate.to_json())

        return jsonify({'flight_gates': flight_gates})

    @app.route('/goshna/api/flight_gates', methods=['POST'])
    def create_flight_gate():
        if not request.json or not 'gate_id' in request.json or not 'flight_id' in request.json:
            abort(400)
        
        gate_id = request.json['gate_id']
        flight_id = request.json['flight_id']
        result = ApiFunctions.post_db("INSERT INTO flight_gates VALUES (NULL, ?, ?)", [gate_id, flight_id]);
        inserted_id = c.lastrowid
        print u'Inserted new flight_gate at row ' + str(inserted_id)
        return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/flight_gates/<int:flight_gate_id>', methods=['DELETE'])
    def delete_flight_gate(flight_gate_id):
        ApiFunctions.post_db("DELETE FROM flight_gates WHERE id=?", [flight_gate_id])
        print u'Deleted listening_user with ID ' + str(inserted_id)
        return jsonify({'result': True})

