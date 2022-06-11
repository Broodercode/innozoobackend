import sys
from flask import Flask, request, jsonify
from db_helpers import run_query
app = Flask(__name__)

@app.route('/')
def homepage():
    return "okay"

@app.get('/api/animals')
def animals_get():
    # TODO db select
    animal_list = run_query("SELECT * FROM animals")
    resp = []
    for animal in animal_list:
        an_obj = {}
        an_obj['id'] = animal[0]
        an_obj['animalName'] = animal[1]
        an_obj['imageURL'] = animal[2]
        resp.append(an_obj)
    return jsonify(animal_list), 200

@app.post('/api/animals')
def animals_post():
    data = request.json
    animal_name=data.get('animalName')
    image_url=data.get('animalURL')
    if not animal_name:
        return jsonify("Missing required argument 'animalName'"), 422
    if not image_url:
        return jsonify("Missing required argument 'imageURL'"), 422
    else:
        run_query("INSERT INTO animals (animalName, imageURL) VALUES(?,?)", [animal_name, image_url])
        return 'added successfully'
    # TODO: DB something
    
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print('Missing required mode argument')
    exit()
    
if mode == 'testing':
    from flask_cors import CORS 
    CORS(app)
    app.run(debug=True)
elif mode == 'production':
    import bjoern
    bjoern.run(app, "0.0.0.0", .5005)
else:
    print("mode must be in testing|production")
    exit()
# def animals_get():
#     print('arrived in animals_get function')
#     db_helpers.run_query("SELECT * FROM p")