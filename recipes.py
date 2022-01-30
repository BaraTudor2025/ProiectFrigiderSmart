import http.client
import json

conn = http.client.HTTPSConnection("api.spoonacular.com")


# Return 'n' recipes for a list of ingredients
def find_recipes_by_ingredients(ingredients, number):

    api_key = '&apiKey=6a25563380ae46dfbb0a50c987c59bea'
    header = '/recipes/findByIngredients?ingredients='
    for i in range(0,len(ingredients)):
        if i == 0:
            header += ingredients[i]
        else:
            header += ',+' + ingredients[i]
    header += api_key
    header += '&number=' + str(number)
    conn.request("GET", header)

    res = conn.getresponse()
    data = res.read()

    list_of_recipes = []
    data_as_json = json.loads(data.decode("utf-8"))
    for i in range(len(data_as_json)):
        recipe = data_as_json[i]['id']
        list_of_recipes.append(recipe)
    return list_of_recipes

# Returns a list of steps for a certain recipe
def get_analyzed_recipe(recipe):
    # api_key = '?apiKey=6a25563380ae46dfbb0a50c987c59bea'
    # header = '/recipes/'
    # header += str(recipe) + '/analyzedInstructions'
    # # header += '/analyzedInstructions'
    # header += api_key
    header = f"/recipes/{str(recipe)}/analyzedInstructions?apiKey=6a25563380ae46dfbb0a50c987c59bea"
    conn.request("GET", header)

    res = conn.getresponse()
    data = res.read()
    steps = []
    data_as_json = json.loads(data.decode("utf-8"))
    for step in data_as_json[0]['steps']:
        steps.append(step['step'])
    return steps
    #GET https://api.spoonacular.com/recipes/324694/analyzedInstructions

print(find_recipes_by_ingredients(['apples', 'flour', 'sugar', 'sausage', 'beef'], 6))
print(*get_analyzed_recipe(640352), sep = "\n")