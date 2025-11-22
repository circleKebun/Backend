from flask import jsonify, make_response


def success(values, message):
    res = {
        'data' : values,
        'message' : message
        
    }
    