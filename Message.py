from flask import Flask, jsonify, abort, request
from Server import *
import ApiFunctions

class Message:
    def __init__(self, id, body, time, flight_id):
        self.id = id
        self.body = body;
        self.time = time;
        self.flight_id = flight_id;

    def to_json(self):
        return {
            'id': self.id,
            'body': self.body,
            'time': self.time,
            'flight_id': self.flight_id
        }

    @app.route('/goshna/api/messages', methods=['GET'])
    def get_messages():
        messages = []
        results = ApiFunctions.query_db("SELECT * FROM messages")
        for row in results:
            message = Message(row['id'], row['body'], row['time'], row['flight_id'])
            messages.append(message.to_json())

        return jsonify({'messages': messages})

    @app.route('/goshna/api/messages/<int:message_id>', methods=['GET'])
    def get_message(message_id):

        row = ApiFunctions.query_db("SELECT * FROM messages WHERE id = ?", [message_id], one=True)
        if row is None:
            abort(404)

        message = Message(row['id'], row['body'], row['time'], row['flight_id'])
        return jsonify({'message': message.to_json()})

    # @app.route('/goshna/api/messages', methods=['POST'])
    # def create_message():
	# 	if not request.json or not 'body' in request.json or not 'time' in request.json or not 'gate_id' in request.json:
	# 		abort(400)

	# 	body = request.json['body']
	# 	time = request.json['time']
	# 	flight_id = request.json['flight_id']

	# 	flights = ApiFunctions.query_db("SELECT flight_id from flight_gates where gate_id=?", [gate_id]);

	# 	# TODO: Check for upcoming flights

	# 	for row in flights:
	# 		flight_id = row['flight_id']
	# 		ApiFunctions.post_db("INSERT INTO messages VALUES (NULL, ?, ?, ?)", [body, time, flight_id]);

	# 	inserted_id = c.lastrowid

	# 	print u'Inserted new message at row ' + str(inserted_id)
	# 	return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/messages/<int:message_id>', methods=['DELETE'])
    def delete_message(message_id):
        ApiFunctions.post_db("DELETE FROM messages WHERE id=?", [message_id])
        print u'Deleted message with ID ' + str(inserted_id)
        return jsonify({'result': True})
