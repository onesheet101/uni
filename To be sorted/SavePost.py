from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

class Post:

    def __init__(self, db):
        self.db = db

    def savePost(self, userID, text, photo, public):
        query = "INSERT INTO Post (userID, Text, Photo, Public) VALUES (%s, %s, %s, %s)"
        try:
            self.db.execute(query, (userID, text, photo, public))
            self.db.commit()
            return jsonify({'message': 'Post saved successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Post not saved'}), 500
        
    def deletePost(self, postID):
        query = "DELETE FROM Post WHERE PostID = %s"
        try:
            self.db.execute(query, (postID))
            self.db.commit()
            return jsonify({'message': 'Post deleted successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Post not deleted'}), 500
        
    def saveReview(self, userID, stars, public, text):
        query = "INSERT INTO Review (userID, Stars, Public, Text) VALUES (%s, %s, %s, %s)"
        try:
            self.db.execute(query, (userID, stars, public, text))
            self.db.commit()
            return jsonify({'message': 'Review saved successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Review not saved'}), 500
    
    def deleteReview(self, reviewID):
        query = "DELETE FROM Review WHERE ReviewID = %s"
        try:
            self.db.execute(query, (reviewID))
            self.db.commit()
            return jsonify({'message': 'Review deleted successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'review not deleted'}), 500

# Connect to the database
mydb = mysql.connector.connect(
    host=,
    port=,  # Default MySQL port
    user=,
    password=,
    database=,
)
mycursor = mydb.cursor()

post_instance = Post(mycursor)

@app.route('/post/save', methods=['POST'])
def save_post():
    data = request.get_json()
    userID = data.get('UserID')
    text = data.get('Text')
    photo = data.get('Photo')
    public = data.get('Public')
    if userID and public:
        return post_instance.savePost(userID, text, photo, public)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400

@app.route('/post/delete', methods=['POST'])
def delete_post():
    data = request.get_json()
    postID = data.get('PostID')
    if postID:
        return post_instance.deletePost(postID)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400

@app.route('/review/save', methods=['POST'])
def save_review():
    data = request.get_json()
    userID = data.get('UserID')
    stars = data.get('Stars')
    public = data.get('Public')
    text = data.get('Text')
    if userID and public:
        return post_instance.saveReview(userID, stars, public, text)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400

@app.route('/review/delete', methods=['POST'])
def delete_review():
    data = request.get_json()
    reviewID = data.get('ReviewID')
    if reviewID:
        return post_instance.deletePost(reviewID)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400

    
if __name__ == '__main__':
   app.run(debug=True)
