import math
import copy
import numpy
from sklearn.cluster import KMeans as km
import googlemaps as gmaps
from googlemaps import convert
from numba import cuda, jit
import warnings
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

class GoogleMapsAPI:
    fields = ['dine_in', 'price_level', 'serves_beer', 'serves_breakfast', 'serves_dinner', 'serves_lunch', 'serves_wine', 'serves_vegetarian_food', 'wheelchair_accessible_entrance'] # attribute fields of establishment to be added

    placeIDs = [] # initialise placeIDs list
    placeNames = [] # initialise placeNames list

    api_key = ''#Need to use an API key

    def __init__(self, coords, _search1):
        self.search = _search1
        self.currCoords = coords
    
    def getSingleAttribute(self, coord):
        gm = gmaps.Client(key=self.api_key)

        offset = 1 # how much of potential location matches the searchTerm 
        biasRadius = 0 # radius of closeness bias from long/lat of device
        lang = 'None' # set default language - English
        minP = 0 # minimum price range for establishments
        maxP = 4 # maximum price range for establishments
        openNow = False # has to be open now to be added
        placeType = 'bar' # type of establishment
        page_token = 'ATplDJbP_zHMMJ9qiKRPlCVeqhtNFJx60ZO-msVYtwx7NmwpU_b7gqVNBwE7DnPASf8T9zDN8KV811GPBrsBzXkxa0Wqs-hTZyyqMo6jgZCiD2o7hQvYQ2n8DPCXU_0TvEKGvC0dZVKWYb7P-B5wXBWrjiy97j5QsZwkO7_QGDXiNf1Ftdl681nB4GpSd4IkYvnHlUWNCP4YYAm3iFSvK2rPj74XdCSX4Sl1ZhumpPpZFusmjSrRi2DkTLxX1Ye2gI1bkCeJ-ZEQXTfKiVuymKvIDL9-pq2kCwgCC-EpuTfZcqdTwedLS9cflxCIm_IDc2tiAIzHk_JpDuxTG-Y58sneT1ulaPjmhj-BL4m2_FioIMq-59ez5uojU67vMCoi_OckTp4iz0sZJuzt-Bn4PhQXY8KyYpOFhZPXD6Fa5_3bzRwU4W3Pjik7k51QlYyMN5Y2eVcqZNvm'
        searchTerm = ''
        sess_token = ''

        out = gm.places(searchTerm, coord, biasRadius, lang, minP, maxP, openNow, placeType, page_token) # find all establishments with parameters

        add = gm.place(((out['results'])[0])['place_id'], sess_token, self.fields, lang, False, 'most_relevant') # get attributes from each establishment with given parameters

        return [add['result']]
    

@app.route('/getEstablishmentDetails', methods=['GET'])
def GetEstablishmentDetails():
    coords = request.args.get('coordinates')
    g = GoogleMapsAPI(coords, 'pub')

    details = g.getsingleattribute(coords)

    return jsonify({'details': details})

