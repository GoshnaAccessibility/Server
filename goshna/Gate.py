from flask import Flask, jsonify, abort, request
from goshna import *
from goshna import ApiFunctions

class Gate:
    def __init__(self, id, name, airport_id):
		self.id = id
		self.name = name
		self.airport_id = airport_id

    def to_json(self):
		return {'id': self.id, 'name': self.name, 'airport_id': self.airport_id}

    @app.route('/goshna/api/gates', methods=['GET'])
    def get_gates():
        gates = []
        results = ApiFunctions.query_db("SELECT * FROM gates")
        for row in results:
            gate = Gate(row['id'], row['name'], row['airport_id'])
            gates.append(gate.to_json())

        return jsonify({'gates': gates})

    @app.route('/goshna/api/gates', methods=['POST'])
    def create_gate():
        if not request.json or not 'name' in request.json or not 'airport_id' in request.json:
            abort(400)
        
        name = request.json['name']
        airport_id = request.json['airport_id']
        result = ApiFunctions.post_db("INSERT INTO gates VALUES (NULL, ?, ?)", [name, airport_id]);
        inserted_id = c.lastrowid
        print u'Inserted new gate at row ' + str(inserted_id)
        return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/gates/find', methods=['POST'])
    def find_gates():
        if not request.json or not 'id' in request.json:
            abort(400)
        
        airport_id = request.json['id']
        gates = []
        results = ApiFunctions.query_db("SELECT * FROM gates where airport_id=?", [airport_id]);
        for row in results:
            gate = Gate(row['id'], row['name'], row['airport_id'])
            gates.append(gate.to_json())

        return jsonify({'gates': gates})

    @app.route('/goshna/api/gates/<int:gate_id>', methods=['DELETE'])
    def delete_gate(gate_id):
        ApiFunctions.post_db("DELETE FROM gates WHERE id=?", [gate_id])
        print u'Deleted listening_user with ID ' + str(inserted_id)
        return jsonify({'result': True})

