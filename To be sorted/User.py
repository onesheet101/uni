from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

class User:
    def __init__(self, db):
        self.db = db

    def GetDetails(self, ID):
        query = "SELECT Username, Email, TopPubs, TopPints FROM Account WHERE UserID = %s"
        self.db.execute(query,(ID,))
        result = self.db.fetchall()
        if result:
            return jsonify({'Username': result[0][0], 'Email': result[0][1], 'TopPubs': result[0][2], 'TopPints': result[0][3]})
        else:
            return jsonify({'message': 'User not found'}), 404

    def AddDetails(self, username, password, email, top_pubs, top_pints):
        query = "INSERT INTO Account (Username, Password, Email, TopPubs, TopPints) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.db.execute(query, (username, password, email, top_pubs, top_pints))
            self.db.commit()
            return jsonify({'message': 'User added successfully'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'User addition failed'}), 500
    
    def UpdatePubs(self, pubList):#Parsed 3 pub IDs to be updated with
        query = "SET TopPubs IN Account TO %s"
        try:
            self.db.execute(query, (pubList,))
            return jsonify({'message': 'Updated successfully'})
        except:
            return jsonify({'message': 'Error could not be updated'})


@app.route('/user/details', methods=['GET'])
def get_user_details():
    ID = request.args.get('UserID')
    return user_instance.GetDetails(ID)

@app.route('/user/add', methods=['POST'])
def add_user_details():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    top_pubs = data.get('top_pubs')
    top_pints = data.get('top_pints')
    if username and password and email:
        return user_instance.AddDetails(username, password, email, top_pubs, top_pints)
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400

@app.route('/user/update/pubs',methods = ['POST'])
def update_user_pubs():
    pubs = request.args.get('pubID')
    return user_instance.UpdatePubs(pubs)


if __name__ == '__main__':
    app.run(debug=True)

#Majority of this except Update_user_pubs has been added to endpoints.
#This will need to be revisted in tandem with the revision of the Account table.
