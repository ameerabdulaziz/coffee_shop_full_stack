import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# ROUTES

@app.route('/drinks')
def drink_list():
    try:
        drinks = Drink.query.all()
        drinks_short = [drink.short() for drink in drinks]
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drinks_short,
        })
    except:
        abort(500)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drink_detail_list(payload):
    print(payload)
    try:
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drinks_long,
        })
    except:
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def drink_create(payload):
    try:
        data = request.get_json()
        title = data.get('title')
        recipe = data.get('recipe')
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drink.short(),
        })
    except:
        abort(422)


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def drink_detail(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        data = request.get_json()
        title = data.get('title')
        recipe = data.get('recipe')

        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        drink_short = drink.short()
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drink_short,
        })
    except:
        abort(422)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def drink_delete(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            'status_code': 200,
            'success': True,
            'delete': id,
        })
    except:
        abort(422)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(403)
def not_authorized(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Not authorized"
    }), 403
