import http.client
import json
import logging
import urllib.error
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from util import handle_exception

conn = http.client.HTTPSConnection("api.spoonacular.com")

_s_api_key = '6a25563380ae46dfbb0a50c987c59bea'

bp = Blueprint('recepies', __name__)
log = logging.getLogger()

@bp.route('/recipes', methods=['GET'])
#@app.route('/recipes', methods=['GET'])
#@auth.login_required
@handle_exception
def recepies():
    ings = request.args.get('ingredients', type=str)
    ings = ings.split(',')

    log.debug(ings)
    if not ings:
        return jsonify({'status': 'ingredients list required'}), 400
    number = request.args.get('number', type=int, default=5)
    if number <= 0:
        number = 5
    if number > 15:
        number = 15

    try:
        recs = find_recipes_by_ingredients(ings, number)
    except urllib.error.HTTPError as e:
        return jsonify({'status': f"can't find recepies: {e.args}"}), 400

    data = []
    for id, title, used, missed in recs:
        try:
            steps = get_steps_of_recipe(id)
        except urllib.error.HTTPError as e:
            data.append({'name': title, 'error': e.args})

        data.append({
            'name': title,
            'used': used,
            'missing': missed,
            'steps': steps
        })
    return jsonify(data), 200


def find_recipes_by_ingredients(ingredients, number=5) -> list:
    header = f"/recipes/findByIngredients?number={str(number)}&apiKey={_s_api_key}&ingredients={',+'.join(ingredients)}"
    conn.request("GET", header)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    recipes = []
    for recipe in data:
        used = [ing['name'] for ing in recipe['usedIngredients']]
        missed = [ing['name'] for ing in recipe['missedIngredients']]
        recipes.append((recipe['id'], recipe['title'], used, missed))

    return recipes


def get_steps_of_recipe(recipe):
    header = f"/recipes/{str(recipe)}/analyzedInstructions?apiKey={_s_api_key}"
    conn.request("GET", header)

    res = conn.getresponse()
    data = res.read()
    steps = []

    data_as_json = json.loads(data.decode("utf-8"))
    for step in data_as_json[0]['steps']:
        steps.append(step['step'])
    return steps
    #GET https://api.spoonacular.com/recipes/324694/analyzedInstructions


# print(find_recipes_by_ingredients(['apples', 'flour', 'sugar', 'sausage', 'beef'], 6))
# print(*get_analyzed_recipe(640352), sep = "\n")