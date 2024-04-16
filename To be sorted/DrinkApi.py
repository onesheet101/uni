from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

class Drink:
    def __init__(self, db):
        self.db = db

    def get_percentage(self, drink_id):
        query = "SELECT Percentage FROM Drink WHERE ID = %s"
        self.db.execute(query, (drink_id,))
        result = self.db.fetchone()
        if result:
            percentage = result[0]
            return percentage
        else:
            return None

    def get_info(self, drink_id, query):
        self.db.execute(query, (drink_id,))
        result = self.db.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    def add_drink_info(self, query, value):
        try:
            self.db.execute(query, (value,))
            self.db.commit()
            return jsonify({'message': 'Drink added successfully'}) 
        except Exception as e:
            print(e)
            return jsonify({'message': 'Drink addition failed'}), 500

# Connect to the database
mydb = mysql.connector.connect(
    host=,
    port=,  # Default MySQL port
    user=,
    password=,
    database=
)

mycursor = mydb.cursor()

# Instantiate the Drink class with the database cursor
drink_instance = Drink(mycursor)

@app.route('/drink/percentage', methods=['GET'])
def get_drink_percentage():
    if request.method == 'GET':
        drink_id = request.args.get('drinkID')
        percentage = drink_instance.get_percentage(drink_id)
        if percentage is not None:
            return jsonify({'percentage': percentage})
        else:
            return jsonify({'message': 'Drink not found'}), 404

@app.route('/drink/name', methods=['GET'])
def get_drink_info():
    if request.method == 'GET':
        drink_id = request.args.get('drinkID')
        query = "SELECT name FROM Drink WHERE ID = %s"
        name = drink_instance.get_info(drink_id, query)
        if name is not None:
            return jsonify({'name': name})
        else:
            return jsonify({'message': 'Drink not found'}), 404

@app.route('/drink/price', methods=['GET'])
def get_drink_price():
    drink_id = request.args.get('drinkID')
    query = "SELECT price FROM Drink WHERE ID = %s"
    return drink_instance.get_info(drink_id, query)

@app.route('/drink/country', methods=['GET'])
def get_drink_country():
    drink_id = request.args.get('drinkID')
    query = "SELECT country FROM Drink WHERE ID = %s"
    return drink_instance.get_info(drink_id, query)

@app.route('/drink/logo', methods=['GET'])
def get_drink_logo():
    drink_id = request.args.get('drinkID')
    query = "SELECT logo FROM Drink WHERE ID = %s"
    return drink_instance.get_info(drink_id, query)

@app.route('/drink/add', methods=['POST'])
def add_drink_info():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    country = data.get('country')
    query = "INSERT INTO Drink (Name, Price, Country) VALUES (%s, %s, %s)"
    if name:
        return drink_instance.add_drink_info(query, (name, price, country))
    else:
        return jsonify({'message': 'Invalid data supplied'}), 400


@app.route('/drink/update/', methods =['POST'])
def update_drink_att():
    data = request.get_json()
    if data.get('name'):#Update name 
        pass
    if data.get('price'):
        pass 
    if data.get('country'):
        pass
    if data.get('logo'):
        pass 

if __name__ == '__main__':
    app.run(debug=True)
