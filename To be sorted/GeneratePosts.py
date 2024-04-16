import mysql.connector
from flask import Flask, request, jsonify
import PersonalPosts #recommended posts and friends posts

class PostNotFoundException(Exception):
    
    def __init__():
        print("Exception occurred: Post not found")

class Generate:
    #static generation of posts
    # - Take list of postID's and format and order so that x amount are on a page and more can be generated
    # Need a message if no more posts can be shown

    bufferSize = 20

    def __init__(self, db, posts : list):
        self.db = db
        self.posts = posts

    def formatPost(self, postID):
        
        username = self.getUsername(self.getUserID(postID))
        time = self.getTime(postID)
        text = self.getText(postID)
        photo = self.getPhoto(postID)
        likes = self.getUsername(self.getLikeList)
        estabID = self.getEstablishmentID(postID)

        out = []
        out.append(username, text, time)
        return out

    
    def getData(self, posts : list) -> list:
        #get post data for the list of postID's

        try:
            query = 'SELECT UserID, Time, Text, Photo, LikeList, EstablishmentID FROM Post WHERE PostID=%s'

            self.allPosts = []

            for i in posts:
                self.db.execute(query, i)
                self.allPosts.append(self.db.fetchall())

            return self.allPosts
        
        except Exception as e:
            print(e)
            return 'Exception Occured: Unable to retrieve posts'
    #fetchall returns a list of tuples -> where each tuple is a row from the database

    def getPostAttribute(self, postID, index):
        for i in self.allPosts:
            if i[0] == postID:
                return i[index]
            else:
                raise PostNotFoundException
    
    def getUserID(self, postID):
        return str(self.getPostAttribute(postID, 0))
    
    def getTime(self, postID):
        return str(self.getPostAttribute(postID, 1))
    
    def getText(self, postID):
        return str(self.getPostAttribute(postID, 2))
    
    def getPhoto(self, postID):
        return str(self.getPostAttribute(postID, 3))
    
    def getLikeList(self, postID):
        return str(self.getPostAttribute(postID, 4))
    
    def getEstablishmentID(self, postID):
        return str(self.getPostAttribute(postID, 5))
    
    def setBufferSize(self, val):
        self.bufferSize = val
    
    def getBufferSize(self):
        return self.bufferSize
    
    def load_posts(self):

        posts = self.getData(self.posts)
        selectedPosts = []

        amount = max(self.bufferSize, len(posts))

        for i in range(amount):
            selectedPosts.append(self.formatPost(posts[i]))

        return selectedPosts
    
    def getUsername(self, userIDList):
        #given a list of user IDs find the account username that it corresponds to - accept lists of 1 also
        
        query = 'SELECT Username FROM Account WHERE UserID=%s'

        usernames = []
        for i in userIDList:
            self.db.execute(query, i)
            usernames.append(self.db.fetchall())

        return usernames 

#TODO
#Complete format for posts to be displayed for users
    

app = Flask(__name__)

# Connect to database
mydb = mysql.connector.connect(
    host=,
    port=,  # Default MySQL port
    user=,
    password=,
    database=,
)
mycursor = mydb.cursor()

@app.route('/feed/generateForYouPosts', method=['GET'])
def generateForYouPosts():

    userID = request.args.get('UserID')
    fyPosts = PersonalPosts.ForYou.getRecommendedPosts(userID)
    gen = Generate(mycursor, fyPosts)
    loadedPosts = gen.load_posts()

    return jsonify({'username': loadedPosts[0]}, {'text': loadedPosts[1]}, {'time': loadedPosts[2]})

@app.route('/feed/generateAllPosts', method=['GET'])
def generateAllPosts():
    
    allPosts = PersonalPosts.ForYou.getAllPosts()
    gen = Generate(mycursor, allPosts)
    loadedPosts = gen.load_posts()

    return jsonify({'username': loadedPosts[0]}, {'text': loadedPosts[1]}, {'time': loadedPosts[2]})

@app.route('/feed/generateFriendsPosts', method=['GET'])
def generateFriendsPosts():

    friendsPosts = PersonalPosts.ForYou.getFriendsPosts()
    gen = Generate(mycursor, friendsPosts)
    loadedPosts = gen.load_posts()

    return jsonify({'username': loadedPosts[0]}, {'text': loadedPosts[1]}, {'time': loadedPosts[2]})
