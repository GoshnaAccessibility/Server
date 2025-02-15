from flask import Flask, jsonify, abort, request, Response
from Server import *
import ApiFunctions
import DisplayFlight
import Message
import time as time2
import json
from datetime import date, time


class Flight:
    def __init__(self, id, airline_id, dest_airport, flight_number, gate,
                 departure):
        self.id = id
        self.airline_id = airline_id
        self.dest_airport = dest_airport
        self.flight_number = flight_number
        self.gate = gate
        self.departure = departure

    def to_json(self):
        return {
            'id': self.id,
            'airline_id': self.airline_id,
            'dest_airport': self.dest_airport,
            'flight_number': self.flight_number,
            'gate': self.gate,
            'departure': self.departure
        }

    @app.route('/goshna/api/flights', methods=['POST'])
    def create_flight():
        if not request.json or not 'airline_id' in request.json or not 'dest_airport' in request.json or not 'flight_number' in request.json or not 'gate' in request.json or not 'departure' in request.json:
            abort(400)

        airline_id = request.json['airline_id']
        dest_airport = request.json['dest_airport']
        flight_number = request.json['flight_number']
        gate = request.json['gate']
        departure = request.json['departure']

        if not airline_id or not dest_airport or not gate:
            abort(400)

        result = ApiFunctions.post_db("INSERT INTO flights VALUES (NULL, ?, ?, ?, ?, ?)", [airline_id, dest_airport, flight_number, gate, departure]);
        inserted_id = c.lastrowid

        print u'Inserted new flight at row ' + str(inserted_id)
        return jsonify({'id': str(inserted_id)}), 201

    # @app.route('/goshna/api/flights/find', methods=['POST'])
    # def find_flights():
    #     airline_id = 0

    #     if request.json and 'airline_id' in request.json:
    #         airline_id = request.json['airline_id']

    #     if(airline_id == 0):
    #             results = ApiFunctions.query_db("SELECT * FROM flights", [])
    #     else:
    #         results = ApiFunctions.query_db("SELECT * FROM flights where airline_id=?", [airline_id])

    #     flights = []
    #     for row in results:
    #         airline = ApiFunctions.query_db("SELECT * FROM airlines WHERE id = ?", [row['airline_id']], one=True)
    #         dest_airport = ApiFunctions.query_db("SELECT * FROM airports WHERE id = ?", [row['dest_airport_id']], one=True)

    #         flight = DisplayFlight.DisplayFlight(
    #             row['id'],
    #             airline['airline_short'],
    #             dest_airport['airport_short'],
    #             row['flight_number'],
    #             row['gate']
    #             row['departure'],
    #             row['airline_id'],
    #             row['dest_airport_id']
    #         )

    #         flights.append(flight.to_json())

    #     return jsonify({'flights': flights})

    @app.route('/goshna/api/flights/find/<string:gate>', methods=['GET'])
    def find_flight(gate):
            row = ApiFunctions.query_db("SELECT * FROM flights WHERE gate = ?",
                                        [gate], one=True)
            if row is None:
                abort(404)

            airline = ApiFunctions.query_db("SELECT airline_short, airline_full FROM airlines WHERE id = ?", [row['airline_id']], one=True)
            flight = DisplayFlight.DisplayFlight(
                row['id'],
                airline['airline_full'],
                airline['airline_short'],
                row['dest_airport'],
                row['flight_number'],
                row['gate'],
                row['departure']
            )

            return jsonify({'flights': [flight.to_json()]})

    @app.route('/goshna/api/flights', methods=['GET'])
    def get_flights():
        flights = []
        results = ApiFunctions.query_db("SELECT * FROM flights WHERE departure > strftime('%s', 'now') ORDER BY departure")
        for row in results:
            airline = ApiFunctions.query_db("SELECT airline_short, airline_full FROM airlines WHERE id = ?", [row['airline_id']], one=True)
            flight = DisplayFlight.DisplayFlight(
                row['id'],
                airline['airline_full'],
                airline['airline_short'],
                row['dest_airport'],
                row['flight_number'],
                row['gate'],
                row['departure']
            )

            flights.append(flight.to_json())

        return jsonify({'flights': flights})

    @app.route('/goshna/api/flights/<int:flight_id>', methods=['GET'])
    def get_flight(flight_id):
            row = ApiFunctions.query_db("SELECT * FROM flights WHERE id = ?",
                                        [flight_id], one=True)
            if row is None:
                abort(404)

            airline = ApiFunctions.query_db("SELECT airline_short, airline_full FROM airlines WHERE id = ?", [row['airline_id']], one=True)
            flight = DisplayFlight.DisplayFlight(
                row['id'],
                airline['airline_full'],
                airline['airline_short'],
                row['dest_airport'],
                row['flight_number'],
                row['gate'],
                row['departure']
            )

            return jsonify({'flight': flight.to_json()})

    @app.route('/goshna/api/flights/messages/<int:flight_id>', methods=['GET'])
    def get_flight_messages(flight_id):
        try:
            message_results = ApiFunctions.query_db("SELECT * FROM messages WHERE flight_id=? ORDER BY time DESC", [flight_id])

            messages = []
            for row in message_results:
                message = Message.Message(row['id'], row['body'], row['time'],
                                          flight_id)
                messages.append(message.to_json())
            return jsonify({'messages': messages})
        except Exception as e:
            return jsonify({'err': str(e)})

    @app.route('/goshna/api/flights/messages/<int:flight_id>',
               methods=['POST'])
    def create_flight_message(flight_id):
        if not request.json or not 'body' in request.json or not 'time' in request.json:
            abort(400)

        body = request.json['body']
        time = request.json['time']

        if not body:
            abort(400)

        result = ApiFunctions.post_db("INSERT INTO messages VALUES (NULL, ?, ?, ?)", [body, time, flight_id])
        inserted_id = c.lastrowid

        return jsonify({'id': str(inserted_id)}), 201

    @app.route('/goshna/api/flights/<int:flight_id>', methods=['DELETE'])
    def delete_flight(flight_id):
        ApiFunctions.post_db("DELETE FROM flights WHERE id=?", [flight_id])
        print u'Deleted flight with ID ' + str(inserted_id)
        return jsonify({'result': True})

    push_poll = 2.5  # 2.5 seconds
    keep_alive_poll = push_poll * 10  # 25 seconds

    @staticmethod
    def get_messages(flight_id, lastMessageTime):
        if lastMessageTime is None:
            # Get all messages for the given flight
            sQuery = ("SELECT * FROM messages WHERE flight_id=? ORDER BY "
                      "time DESC")
        else:
            # Only get more recent messages since last push to client
            sQuery = ("SELECT * FROM messages WHERE flight_id=? AND time>" +
                      str(lastMessageTime) + " ORDER BY time DESC")
        with app.app_context():
            alive_counter = 0
            while True:  # TODO use blocking/events, not polling
                time2.sleep(push_poll)
                alive_counter = alive_counter + push_poll
                message_results = ApiFunctions.query_db(sQuery, [flight_id])
                if len(message_results) > 0:
                    lastMessageTime = message_results[0]['time']
                    # Format messages fo transport
                    messages = []
                    for row in message_results:
                        message = Message.Message(row['id'], row['body'],
                                                  row['time'], flight_id)
                        messages.append(message.to_json())
                    # Break loop by returning the latest messages
                    # NB no need to use Flask's jsonify object here, as it adds
                    # lots of additional processing bloat for a Response object
                    # (which we do not use or need here for the stream).
                    return [json.dumps({'messages': messages},
                                       separators=(',', ':')),  # Minified
                            lastMessageTime]
                elif alive_counter >= keep_alive_poll:
                    raise IdleConnectionException()

    @app.route('/goshna/api/flights/messages/<int:flight_id>/stream')
    def get_flight_messages_streamed(flight_id):
        '''Streams flight messages using Server-Side Events.'''
        # https://stackoverflow.com/a/51969441/508098
        def event_stream():
            lastMessageTime = None
            while True:
                try:
                    # wait for source data to be available, then push it
                    [sJSON,
                     lastMessageTime] = Flight.get_messages(flight_id,
                                                            lastMessageTime)
                    yield 'data: {}\n\n'.format(sJSON)
                except IdleConnectionException as zce:
                    # TCP keeps connections open even if client no longer
                    # exists; TCP only checks connections on write, not on
                    # read. To test if a subscribed client is still active,
                    # send a simple/small message ('\n') that will be ignored
                    # by the client as it is expecting to see (e.g.) "data: ".
                    # This is a keep-alive, of sorts - I'm certain there must
                    # be a better way to do this.
                    yield '\n'  # Broken pipes will raise an IOError
        return Response(event_stream(), mimetype="text/event-stream")


class IdleConnectionException(Exception):
    pass
