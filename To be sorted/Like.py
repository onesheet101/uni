from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to the database
mydb = mysql.connector.connect(
    host=,
    port=,  # Default MySQL port
    user=,
    password=,
    database=,
)
dbCur = mydb.cursor()
        
@app.route('/post/like', methods=['POST'])
def addlike():

    userID = request.args.get('UserID')
    postID = request.args.get('PostID')

    likeList = getLikeList()

    postLikeQuery = 'INSERT INTO PostLike VALUES(%s, %s)'
    postQuery = 'UPDATE Post SET LikeList=%s WHERE PostID=%s'

    upLikeList = (str(likeList)) + ', ' + str(userID)

    try:
        dbCur.execute(postLikeQuery, (postID, userID))
        dbCur.execute(postQuery, (upLikeList, postID))
        dbCur.commit()

        return jsonify({'message': 'Like added successfully'})
        
    except Exception as e:
        return jsonify({'message': 'Like addition failed'}), 500

@app.route('/post/unlike', methods=['POST'])
def removeLike():

    userID = request.args.get('UserID')
    postID = request.args.get('PostID')

    likeList = getLikeList()

    postLikeQuery = 'DELETE FROM PostLike WHERE(PostID=%s AND UserID=%s)'
    postQuery = 'UPDATE Post SET LikeList=%s WHERE PostID=%s'

    try:
        dbCur.execute(postLikeQuery, (postID, userID))
        dbCur.execute(postQuery, (str(rmvLikeList(likeList, userID)), postID))
        dbCur.commit()

        return jsonify({'message': 'Like removed successfully'})

    except Exception as e:
        return jsonify({'message': 'Like removal failed'}), 500
    

@app.route('/post/likeNumber', methods=['GET'])
def likeNumber():
    try:
        ll = getLikeList().split(',')
        return jsonify({'LikeNumber': len(ll)})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error could not retrieve like number'})

def getLikeList():

    postID = request.args.get('PostID')

    query = 'SELECT LikeList FROM Post WHERE PostID = %s'

    try:
        dbCur.execute(query, postID)
        rslt = dbCur.fetchall()

        return rslt

    except Exception as e:
        return jsonify({'message': 'Failed to retrieve like list'})

def rmvLikeList(lst, val):

    try:
        lst = lst.split(',')
        #out = lst.remove(val)
        out = []
        for i in lst:
            if i != val:
                out.append(i + ',')
        
        sr = ''
        for i in out:
            sr = sr + i

        return sr
    except Exception as e:
        return jsonify({'message': 'Like List Error'})

#TODO:
#Needs final testing