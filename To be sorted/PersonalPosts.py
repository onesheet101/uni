import Recommended
from flask import request, jsonify

class ForYou:

    classNo = 0
    searchTerm = '' #general search term for establishments
    query = 'SELECT PostID,lon,lat FROM Establishment, Post WHERE EstablishmentID == Post.Establishment AND Post.Public == True SORT BY Post.Time DESC;' #SQL query for selecting coordinates of establishments used in public posts
    #Looks at all public posts in the database and then classifies them and gives similair reccomended to user

    def __init__(self, _searchTerm, _classNo, dbCursor):

        #set all class variables upon initiation with parameters
        self.searchTerm = _searchTerm
        self.dbCur = dbCursor
        self.classNo = _classNo

    def databaseQuery(self):
        try:
            self.dbCur.execute(self.query) #execute query to get coordinates of establishments
            res = self.dbCur.fetchall() #store result of the query in res structure
            return res
        except:
            raise Exception('Database Connection Error: Unable to connect to database')
    
    def getRecommendedPosts(self, userID):
        #Uses databaseQuery and gets the coordinates of all public posts
        #Produces single attribute on all of the coordinates
        #then produces a model with them
        #then do the same with liked posts - get them all and classify on the SAME MODEL
        #Choose the most common classification then return all public posts with the same one

        #TODO
        #Format what the database returns and organise the data so that the PostID's are in postIDs list
        # and the coordinates are in the allPublic list

        allPublic = self.databaseQuery()
        allLikedPosts = self.getLikedPosts(userID)

        #Need to see how the database query will return the data
        # We want a list of coordinates and a list of PostID where the Indexes match
        postIDs = []
        pubAttr = []
        for i in allPublic:
            gm = Recommended.GoogleMapsAPI(allPublic[i], 'Pub')
            pubAttr.append(gm.getSingleAttribute(allPublic[i]))
        
        km = Recommended.KMeans()
        data = km.formDataset(pubAttr)
        pred = km.buildModel(data, self.classNo) #Indexes match with the PostID list

        likeClass = []
        for i in allLikedPosts:
            likeClass.append(km.predictClass(i))
        
        #Find most common class in likeClass then filter pred down to only those classes - use index
        #Then return postID with that index
        count = []
        for i in range(max(likeClass)):#Fill count with 0
            count.append(0)

        for i in likeClass:
            count[i] += 1

        topClass = count.index(max(count)) #Most popular class assigned

        selected = []

        for i in range(len(pred)):
            if pred[i] == topClass:
                selected.append(postIDs[i])

        return selected #list of postIds which are recomended

    def classify(self, coords) -> dict:
        #Provides a classification for an establishment given its coordinates and the 20 around it
        gm = Recommended.GoogleMapsAPI(coords, self.searchTerm) #initialise googlemaps API
        km = Recommended.KMeans() #initialise KMeans classification

        data = gm.produceAttributes() #get attributes of establishment with given coordinates
        pID = gm.getPlaceIDs() #get the placeIDs
        cData = km.formDataset(data) #create the dataset for data in the correct format
        classes = km.buildModel(cData, self.classNo) #classify each of the 

        placeClasses = {}
        
        for i in range(len(classes)):
            placeClasses[pID[i]] = classes[i] #dictionary with placeID as key and value is the class of establishment

        return placeClasses #return dictionary


    def sortByClass(self, clas : int, plaCla : dict) -> list:
        #Given an integer which represents the class return all placeIDs of the establishments with that classification value in a list
        out = []

        #Change to binary search
        for i in plaCla.keys():
            if plaCla[i] == clas:
                out.append(i)

        return out # Return a list of all the placeID's with a classification given in the function call
        
        
    def getPostsFromPlaceIDList(self, places : list) -> bool:
        res = []

        for i in places:
            self.dbCur.execute('SELECT PostID FROM Posts WHERE PlaceID=%s') #execute query for selecting all posts from database from the place with placeID
            res.append(self.dbCur.fetchall(), i) #add retrieved data to res structure

        return res
    
    def getAllPosts(self):

        query = 'SELECT PostID FROM Posts'

        self.dbCur.execute(query)
        allPosts = self.db.fetchall()

        return allPosts
    
    def getLikedPosts(self, userID):
        
        query = 'SELECT PostID FROM PostLike WHERE UserID=%s'

        try:
            self.db.execute(query, userID)
            rslt = self.db.fetchall()
            return rslt
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error unable to retrieve liked posts'})
    
    def getPostLocation(self, postID):

        getEstab = 'SELECT EstablishmentID FROM Post WHERE PostID=%s'

        self.db.execute(getEstab, postID)
        estabID = self.db.fetchall()

        getLatLon = 'SELECT Lat, Lon FROM Establishment WHERE ID=%s'

        self.db.execute(getLatLon, estabID)
        latLon = self.db.fetchall()

        return latLon

    def getFriendsPosts(self):

        #TODO
        #Requires Testing
        
        userID = request.args.get('UserID')

        friendsQuery = 'SELECT Friends FROM Account WHERE UserID=%s'
        self.db.execute(friendsQuery, userID)
        friendsList = self.db.fetchall()
        friendsList = friendsList.split(',')

        query = ''
        for i in friendsList:
            query += 'SELECT PostID FROM Post WHERE UserID=' + i + ' UNION JOIN '

        query = query[:len(query)-12]
        query += ' ORDER BY Time ASC'

        self.db.execute(query)
        friendsPosts = self.db.fetchall()

        return friendsPosts

#TODO:
#- Check functionality
#- Add comments

        
        
