#GoogleMapsAPI | 25/02/2024 | Joel Millar

import math
import copy
import numpy
from sklearn.cluster import KMeans as km
import googlemaps as gmaps
from googlemaps import convert
from numba import cuda, jit
import warnings

class GoogleMapsAPI:

    fields = ['dine_in', 'price_level', 'serves_beer', 'serves_breakfast', 'serves_dinner', 'serves_lunch', 'serves_wine', 'serves_vegetarian_food', 'wheelchair_accessible_entrance'] # attribute fields of establishment to be added

    fileNameTrain = 'BarAttributesTrain'
    fileNameTest = 'BarAttributesTest'
    fileType = '.txt'

    placeIDs = [] # initialise placeIDs list
    placeNames = [] # initialise placeNames list

    search = ''
    currCoords = ''
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
        

    def getKeyAttributes(self, searchTerm):

        gm = gmaps.Client(key=self.api_key) # set up client with API key
        
        #searchTerm -> key term to search for places
        offset = 1 # how much of potential location matches the searchTerm
        startLocation = self.currCoords # set longitude and latitude 
        biasRadius = 100 # radius of closeness bias from long/lat of device
        lang = 'None' # set default language - English
        minP = 0 # minimum price range for establishments
        maxP = 4 # maximum price range for establishments
        openNow = False # has to be open now to be added
        placeType = 'bar' # type of establishment
        page_token = 'ATplDJbP_zHMMJ9qiKRPlCVeqhtNFJx60ZO-msVYtwx7NmwpU_b7gqVNBwE7DnPASf8T9zDN8KV811GPBrsBzXkxa0Wqs-hTZyyqMo6jgZCiD2o7hQvYQ2n8DPCXU_0TvEKGvC0dZVKWYb7P-B5wXBWrjiy97j5QsZwkO7_QGDXiNf1Ftdl681nB4GpSd4IkYvnHlUWNCP4YYAm3iFSvK2rPj74XdCSX4Sl1ZhumpPpZFusmjSrRi2DkTLxX1Ye2gI1bkCeJ-ZEQXTfKiVuymKvIDL9-pq2kCwgCC-EpuTfZcqdTwedLS9cflxCIm_IDc2tiAIzHk_JpDuxTG-Y58sneT1ulaPjmhj-BL4m2_FioIMq-59ez5uojU67vMCoi_OckTp4iz0sZJuzt-Bn4PhQXY8KyYpOFhZPXD6Fa5_3bzRwU4W3Pjik7k51QlYyMN5Y2eVcqZNvm' # previous search token

        out = gm.places(searchTerm, startLocation, biasRadius, lang, minP, maxP, openNow, placeType, page_token) # find all establishments with parameters

        for i in out['results']: # loop to add datum to placeNames and placeIDs
            self.placeNames.append((i['name'])) # add to placeNames
            self.placeIDs.append(i['place_id']) # add to placeIDs

        dataAttributes = [] # initialise dataAttributes
        sess_token = 'None' # session token is set to none
        
        for i in self.placeIDs: # loop to add attributes to dataAttributes list
            add = gm.place(i, sess_token, self.fields, lang, False, 'most_relevant') # get attributes from each establishment with given parameters
            
            dataAttributes.append(add['result']) # add attributes to dataAttributes

        return(dataAttributes)


    def correctFormat(self, data):
        # data is the list of dict for the establishment data

        keyList = []
        out = []
        line = ''

        for i in data:
            line = self.alter(i)
            out.append(line)
            line = ''
        return out
            

    def alter(self, data):
        #data should be dictionary of establishment data - single instance

        line = ''
        
        for i in self.fields:
            if self.contains(data.keys(), i): # if data contains the value in fields it will then check the value to return 0 or 1. If not in there it will default to 0
                if data[i] == True:
                    line += '1'
                else:
                    line += '0'
            else:
                line += '0'

        return line


    def contains(self, data, inp):
        #data should be list

        found = False
        for i in data:
            if i == inp:
                found = True
        return found

    def getData(self, data):
         #data should be a list of attributes 1 or 0 of all the same length

        count = len(data[0])
        attr = ''
        out = []

        for i in data:
            for j in range(count):
                attr += i[j] + ' '
            out.append(attr)
            attr = ''
        
        testLen = 5 # add function to calculate number of tests for 
        trainData = out[testLen+1:]
        testData = out[0:testLen]    

    def produceSingleAttribute(self, coords):

        data = self.correctFormat(self.getSingleAttribute(coords))

        count = len(data[0])
        attr = ''
        produceAttr = []

        for i in data:
            for j in range(count):
                attr += i[j] + ' '
            produceAttr.append(attr)
            attr = ''
        
        return produceAttr

    def produceAttributes(self):
        data = self.correctFormat(self.getKeyAttributes(self.search))

        count = len(data[0])
        attr = ''
        produceAttr = []

        for i in data:
            for j in range(count):
                attr += i[j] + ' '
            produceAttr.append(attr)
            attr = ''
        
        return produceAttr
    
    def getDistanceTo(self, sp, ep):
        #Gets the distance between sp and ep
        gmaps = gmaps.Client(key=self.api_key)
        result = gmaps.distance_matrix(sp, ep)
        distanceInM = result['rows'][0]['elements'][0]['distance']['text']
        return distanceInM

    def getTimeTo(self, sp, ep):
        #get the time it takes to go from sp to ep
        gmaps = gmaps.Client(key=self.api_key)
        result = gmaps.distance_matrix(sp, ep)
        time_taken = result['rows'][0]['elements'][0]['duration']['text']
        return time_taken

    def getSearch(self):
        return self.search

    def getPlaceNames(self):
        return self.placeNames

    def getPlaceIDs(self):
        return self.placeIDs


class KMeans:

    model = ''

    def getDataset(self, filename):
        data = ''
        try:
            f = open(filename, 'r')
            data = f.read()
        except:
            print('Error Reading File')

        content = data.splitlines()
        
        data = []

        for i in content:
            data.append(i.split())

        #Data is array of arrays with attributes

        numpyArrs = []

        for i in data:
            numpyArrs.append(numpy.array(i))

        return numpyArrs


    def formDataset(self, data):
        out = []
        numpyArrs = []

        for i in data:
            out.append(i.split())

        for i in out:
            numpyArrs.append(numpy.array(i))

        return numpyArrs
        
        

    def buildModel(self, data, n_clusters):

        model = km(n_init=n_clusters, n_clusters=n_clusters)
        self.model = model

        model.fit(data)

        all_pred = model.predict(data)

        return all_pred
    

    def predictClass(self, coords):

        getSingle = GoogleMapsAPI(coords, '')

        datum = self.formDataset(getSingle.produceSingleAttribute(coords))
       
        prediction = self.model.predict(datum)

        return prediction


    def getModel(self):
        return self.model



class Route:

    startPoint = ''
    noOfEstab = 0
    searchTerm = ''
    finalRoute = []
    prevResult = []

    warnings.filterwarnings('ignore')
    
    def __init__(self, startPoint_, noOfEstab_ : int, searchTerm_ : str):
        self.startPoint = startPoint_
        self.noOfEstab = noOfEstab_
        self.searchTerm = searchTerm_
        

    @jit(target_backend='cuda')
    def createRoute(self, sp, classNo):

        correctPlaces = []
        kme = KMeans()
        gm = GoogleMapsAPI(sp, self.searchTerm)
        estabs = kme.formDataset(gm.produceAttributes())
        placeNames = gm.getPlaceNames()
        pred = kme.buildModel(estabs, classNo)

        iniPred = kme.predictClass(sp)

        for i in range(len(pred)-1):
            if iniPred == pred[i]:
                correctPlaces.append(placeNames[i])

        correctPlaces = self.removeDuplicates(correctPlaces)

        if len(correctPlaces) >= self.noOfEstab:
            self.finalRoute = correctPlaces[:self.noOfEstab]
            return True #need to only return number of estab amount
        else:
            self.createRoute(sp, (classNo - 1))

    @jit(target_backend='cuda')
    def removeDuplicates(self, data):

        out = []

        for i in data:
            if not(i in out):
                out.append(i)
        return out
                

    def getStartPoint(self):
        return self.startPoint

    def getNoOfEstab(self):
        return self.noOfEstab

    def getFinalRoute(self):
        return self.finalRoute


#TODO: Implement a distance check function which checks that the next appropriate establishment is not next door or too far away
