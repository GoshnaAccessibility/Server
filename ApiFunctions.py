from goshna import *
from flask import make_response, jsonify

# Standard function
def query_db(query, args=(), one=False):
    cur = c.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def post_db(query, args=(), one=False):
    cur = c.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    conn.commit()
    return (rv[0] if rv else None) if one else rv

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

