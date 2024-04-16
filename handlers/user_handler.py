from flask import jsonify

def GetDetails(user_id, db):
    with db.cursor() as cursor:
        query = "SELECT Username, Email, TopPubs, TopPints FROM Account WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

    if result:
        return jsonify({'Username': result[1], 'Email': result[3], 'TopPubs': result[4], 'TopPints': result[5]})
    else:
        return jsonify({'message': 'User not found'}), 404

def AddDetails(username, email, top_pubs, top_pints):
    query = "INSERT INTO Account (Username, Password, Email, TopPubs, TopPints) VALUES (%s, %s, %s, %s, %s)"
    try:
        self.db.execute(query, (username, password, email, top_pubs, top_pints))
        self.db.commit()
        return jsonify({'message': 'User added successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'User addition failed'}), 500