import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

class Friend:

    def __init__(self, db):
        
        self.db = db
    
    def following(self, userID):
        #get following list
        
        try:
            query = 'SELECT Friends FROM Account WHERE UserID=%s'

            self.db.execute(query, userID)
            
            foll = self.db.fetchall()
            foll = foll.split(',')

            return foll
        except Exception as e:
            print(e)
            return False

    
    def followers(self, userID):
        #get followers list

        #TODO

        try:
            query = 'SELECT UserID FROM Account'
            self.db.execute(query)
            ids = self.db.fetchall()

            fllIDs = []
            for i in ids:
                if self.isFollowing(i):
                    fllIDs.append(i)
            
            return fllIDs
            
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error: unable to get followers'})
        

    def getFollowingCount(self, userID):
        try:
            query = 'SELECT COUNT(Friends) FROM Account WHERE UserID=%s'

            self.db.execute(query, userID)
            n = self.db.fetchall()

            return int(n)
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error: unable to get following count'})

    def getfollowerCount(self, userID):

        try:
            query = 'SELECT UserID FROM Account'
            self.db.execute(query)
            ids = self.db.fetchall()

            count = 0
            for i in ids:
                if self.isFollowing(i):
                    count += 1
            
            return count
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error: unable to get follower count'})
    
    def isFollowing(self, userID, targetID):
        
        fl = self.following()

        if targetID in fl:
            return True
        else:
            return False

    
    def beginFollowing(self, toFollowID, userID):
        #add user to friend list
        
        try:
            if not(self.isFollowing(userID, toFollowID)):
                query = 'UPDATE Account SET VALUES(Friends=%s) WHERE UserID=%s'

                self.db.execute(query, str(self.getFollowing()) + ',' + str(toFollowID), userID)
                self.db.commit()
                return toFollowID
            else:
                #already following so dont query database just return as if successful i.e. nothing will happen
                return toFollowID
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error: unable to follow ' + str(toFollowID)})
    
    def stopFollowing(self, targetID, userID):
        #remove user from friend list
        
        try:
            query = 'UPDATE Account SET VALUE(Friends=%s) WHERE UserID=%s'

            self.db.execute(query, self.removeFromFriends(targetID), userID)
            self.db.commit()

            return targetID
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error: unable to stop following ' + str(targetID)})
    
    def removeFromFriends(self, targetID, userID):

        try:
            query = 'SELECT Friends FROM Account WHERE UserID=%s'

            self.db.execute(query, userID)
            lst = self.db.fetchall()

            lst = lst.split(',')
            out = []

            for i in lst:
                if i != targetID:
                    out.append(i + ',')
            
            sr = []
            for i in out:
                sr = sr + i
            
            return sr
        except Exception as e:
            print(e)

# Connect to the database
mydb = mysql.connector.connect(
    host=,
    port=,
    user=,
    password=,
    database=,
)
mycursor = mydb.cursor()

fr = Friend(mycursor)

#Need to request.args.get(UserID) in each method

@app.route('/getFollowing', method=['GET'])
def getFollowing():
    
    userID = request.args.get('UserID')

    return jsonify({'FollowingList': fr.following(userID)})

@app.route('/getFollowers', method=['GET'])
def getFollowers():
    
    userID = request.args.get('UserID')

    return jsonify({'FollowersList': fr.followers(userID)})


@app.route('/getFollowingCount', method=['GET'])
def getFollowingCount():

    userID = request.args.get('UserID')

    return jsonify({'FollowingCount': fr.getFollowingCount(userID)})


@app.route('/getFollowersCount', method=['GET'])
def getFollowersCount():
    
    userID = request.args.get('UserID')
    return jsonify({'FollowerCount': fr.getfollowerCount(userID)})

@app.route('/followUser', method=['GET'])
def followUser():
    
    userID = request.args.get('UserID')
    targetID = request.args.get('toFollowID')

    fr.beginFollowing(userID, targetID)
    return jsonify({'message': 'You are now following ' + str(targetID) + '!'})

@app.route('/unfollowUser', method=['GET'])
def unfollowUser():
    
    userID = request.args.get('UserID')
    targetID = request.args.get('toFollowID')

    fr.stopFollowing(userID, targetID)
    return jsonify({'message': 'You have unfollowed ' + str(targetID) + '!'})


#TODO

#Final Testing
#Most of the endpoints have been added into endpoint.py but again they will need to be rejigged to fit overall and
#some table they access will need to be made.
#Mainly a following table.