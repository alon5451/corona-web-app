from data-scraping.place import Place
from data-scraping.department import Department
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

google_api_key = 'AIzaSyDkG702RFFEEm08CP87sLK_amm-ru_eUVs'

@app.route('/', methods=['GET'])
def home():
    return render_template('/index.html', google_api_key = google_api_key)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        placeName = request.args['search']
        query = ''
    except:
        query = request.args['query']
        placeName = 'null'
    print(placeName, query)
    return render_template('/dashboard.html', placeName=placeName, query=query, google_api_key=google_api_key)

@app.route('/place', methods=['GET'])
def get_place():
    placeName = request.args['name']
    place = Place(placeName)
    props = place.set_props()
    if 'error' in props.keys():
        return props

    place.google_api()
    # place.set_general_hours()
#     alerts = list(get_alerts(fromDate, toDate).apply(lambda x: x.to_json(force_ascii=False), axis=1))
    
    return place.get_props()

@app.route('/department', methods=['GET'])
def get_places():
    query = request.args['query']
    placesList = Department(query).google_api_list()

    # place.set_general_hours()
#     alerts = list(get_alerts(fromDate, toDate).apply(lambda x: x.to_json(force_ascii=False), axis=1))
    print(placesList)
    return str(placesList)

# app.run(debug=True, port=9090, use_reloader=True)
app.run(port=9090)