from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

class Comment:

    def __init__(self, db):
        self.db = db

    def saveComment(self, postID, CommenterID, text):
        query = "INSERT INTO PostComment (PostID, CommenterID, Text) VALUES (%s, %s, %s)"
        try:
            self.db.execute(query, (postID, CommenterID, text))
            self.db.commit()
            return jsonify({'message': 'Comment saved successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Comment not saved'}), 500
        
    def deleteComment(self, postID, CommenterID):
        query = "DELETE FROM PostComment WHERE (PostID = %s AND CommenterID = %s)"
        try:
            self.db.execute(query, (postID, CommenterID))
            self.db.commit()
            return jsonify({'message': 'Comment deleted successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Comment not deleted'}), 500

# Connect to the database
mydb = mysql.connector.connect(
    host=,
    port=,  # Default MySQL port
    user=,
    password=,
    database=,
)
mycursor = mydb.cursor()

post_instance = Comment(mycursor)

@app.route('/comment/save', methods=['POST'])
def save_comment():
    data = request.get_json()
    postID = data.get('PostID')
    commenterID = data.get('CommenterID')
    text = data.get('Text')
    if postID and commenterID:
        return post_instance.saveComment(postID, commenterID, text)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400

@app.route('/comment/delete', methods=['POST'])
def delete_comment():
    data = request.get_json()
    postID = data.get('PostID')
    commenterID = data.get('CommenterID')
    if postID and commenterID:
        return post_instance.deleteComment(postID, commenterID)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400
    
    
if __name__ == '__main__':
   app.run(debug=True)