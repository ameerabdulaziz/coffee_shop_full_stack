import sqlalchemy
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# ROUTES

@app.route('/drinks')
def drink_list():
    """
    This endpoint returns all drinks in a pretty representation
    :return: drinks_short
    """
    try:
        drinks = Drink.query.all()
        drinks_short = [drink.short() for drink in drinks]
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drinks_short,
        })
    except NameError:
        abort(422)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drink_detail_list(payload):
    """
    This endpoint returns all drinks detail with a permission required
    :return: drinks_long
    """
    try:
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drinks_long,
        })
    except NameError:
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def drink_create(payload):
    """
    This endpoint creates a new drink with a permission required
    :return: drinks_short
    """
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
    except sqlalchemy.exc.IntegrityError:
        abort(422)


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def drink_detail(payload, id):
    """
    This endpoint edits a specific drink with a permission required
    :return: drinks_long
    """
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
        drink_long = drink.long()
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': drink_long,
        })
    except NameError:
        abort(422)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def drink_delete(payload, id):
    """
    This endpoint deletes a specific drink with a permission required
    :return: id
    """
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
    except AttributeError:
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


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Receive the raised authorization error and propagates it as response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
