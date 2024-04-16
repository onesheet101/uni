from flask import request
from handlers.password_handler import *
from handlers.user_handler import *
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from handlers.friend_handler import *

def setup_endpoints(app, jwt, db):

    #-------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------PASSWORD HANDLING---------------------------------------------------
    @app.route('/login', methods=['POST'])
    def login():

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        #Check if fields are empty.
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        #If the user is authenticated create a token that lasts for thirty minutes and return it to them.
        if authenticate_user(username, password, db):
            expires = timedelta(minutes=180)
            access_token = create_access_token(identity=username, expires_delta=expires)
            return jsonify({'message': 'Login successful'}), 200, {'Authorization': access_token}
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    @app.route('/change-password', methods=['POST'])
    def change_password():

        data = request.json
        username = data.get('username')
        password = data.get('password')
        new_password = data.get('new_password')

        if not check_user_pass_validity(new_password):
            return jsonify({"error": "New password format incorrect"}), 400

        if authenticate_user(username, password, db):
            hashed_password = hash_password(new_password)

            update_password(username, hashed_password, db)
            return jsonify({'message': 'Password change successful'}), 200

        return jsonify({'error': 'Invalid username or password'}), 401

    @app.route('/register', methods=['POST'])
    def register():
        user_table = "users"
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
    
        #Checks if any fields are empty again.
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        #check and see if username exists in database need to set up interface!!!
        # If user exists return error code and message.
        if does_user_exist(username, user_table, db):
            return jsonify({"error": "User already exists"}), 409

        if not check_user_pass_validity(password):
            return jsonify({"error": "Password format incorrect"}), 400
        if not check_user_pass_validity(username):
            return jsonify({"error": "Username format incorrect"}), 400
        hashed_password = hash_password(password)

        #store hashed_password with the username in the database again need to work on implementing database functionality.
        store_password(username, hashed_password, db)

        return jsonify({"message": "User registered successfully"}), 201

# -------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------USER DETAILS---------------------------------------------------------

    @app.route('/user-details', methods=['GET'])
    def get_user_details():
        data = request.get_json()
        user_id = data.get('user_id')
        return GetDetails(user_id, db)

    @app.route('/user-add', methods=['POST'])
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
            return jsonify({'error': 'Invalid data supplied'}), 400

# -------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------FRIENDS--------------------------------------------------------

    @app.route('/getFollowing', method=['GET'])
    def getFollowing():
        data = request.get_json()
        userID = data.get('UserID')

        followers = following(userID)
        if followers:
            return jsonify({'data': followers}), 200
        return jsonify({'error': 'Unable to retrieve following'}), 400

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

    #----------------------------------------------------------------------------------------------------
  #This was just a test endpoint for using tokens. Going to keep it for now just for reference.
    @app.route('/requires-token', methods=['GET'])
    @jwt_required()
    def requires_token():
        current_user = get_jwt_identity()
        message = f'User has valid token: {current_user}'
        return jsonify({'message': message}), 200






