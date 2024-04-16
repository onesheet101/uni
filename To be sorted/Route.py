from flask import Flask, jsonify, request
import mysql.connector
import Recommended

# Connect to the database
mydb = mysql.connector.connect(
    host=,
    port=,  # Default MySQL port
    user=',
    password=,
    database=,
)
dbCur = mydb.cursor()

app = Flask(__name__)
    
searchTerm = 'Pub'

@app.route('/map/getRecommendedEstablishments', methods=['GET'])
def getRecommendedestablishments():

    #takes input coordinates and then produces establishments with the same classification around it

    try:
        startPoint = request.args.get('Start Point')
        re = Recommended.GoogleMapsAPI(startPoint, searchTerm)
        km = Recommended.KMeans()
        attr = re.produceAttributes()
        attr = km.formDataset(attr)
        names = re.getPlaceNames()
        pred = km.buildModel(attr, 7)
        prediction = km.predictClass(startPoint)

        recommendedEstabs = sortClass(prediction, pred, names)

        return jsonify({'RecommendedEstablishments': str(recommendedEstabs)})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Unable to produce recommeneded establishments'})

@app.route('/map/getRouteLocations', methods=['GET'])
def getRouteLocations():

    #produces x number of establishment names for the route planener

    try:
        startPoint = request.args.get('Start Point')
        distance = request.args.get('Distance')
        rt = Recommended.Route(startPoint, distance, searchTerm)
        rt.createRoute(startPoint, 7)
        locations = rt.getFinalRoute()
        return jsonify({'MapLocations': str(locations)})
    except Exception as e:

        return jsonify({'message': 'Unable to create route'})
    
@app.route('/saveRoute', methods=['POST'])
def saveRoute():
    #Take a list of establishments, convert them to a comma seperated string then save to database

    try:

        route = request.args.get('Route')
        userID = request.args.get('UserID')
        rte = []
        for i in route:
            rte.append(str(i) + ',')

        query = 'UPDATE SavedRoutes SET VALUES(COUNT(RouteID) + 1, %s, %s, %s, %s)'
        dbCur.execute(query, 0, len(route), route, 0, userID)
        dbCur.commit()

        return jsonify({'message': 'Route saved successfully'})
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error: Unable to save route'})
    

def sortClass(pred, data, names):
    rec = []
    for i in range(len(data)):
        if data[i] == pred:
            rec.append(names[i])
    return rec



#TODO
#Final testing
