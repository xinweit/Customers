from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import datetime
import jwt


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/customers'
app.config['SECRET_KEY'] = 'secretkey'
app.debug=True
db=SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, dob):
        self.name = name
        self.dob = dob
        self.updated_at = datetime.datetime.now()

db.create_all()
db.session.commit()

def token_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        
        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        try:   
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message' : 'Token is invalid'}), 403
        
        return f(*args, **kwargs)
    return wrapped

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'Only authorized users are allowed.'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
        app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    
    return make_response('Authentication failed.', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})

# Create a customer
@app.route('/customers', methods=['POST'])
@token_required
def add_customer(): 
    customer_data = request.get_json()
    date = customer_data['dob'].split("-",2)
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])

    customer = Customer(name = customer_data['name'], dob = datetime.date(year, month, day))
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer_data)

# Read all customers
@app.route('/customers', methods=['GET'])
@token_required
def get_all_Customers():
    customers_list = []
    customers = Customer.query.all()
    for customer in customers:
        current_customer = {}
        current_customer['id'] = customer.id
        current_customer['name'] = customer.name
        current_customer['dob'] = customer.dob
        current_customer['updated_at'] = customer.updated_at
        customers_list.append(current_customer)
    return jsonify(customers_list)

# Update a customer
@app.route('/customers', methods=['PUT'])
@token_required
def update_customer():
    id_to_update = int(request.args.get('update_id', None))
    updated_customer_data = request.get_json()
    updated_name = updated_customer_data['name']
    print(updated_name)
    updated_date = updated_customer_data['dob'].split("-",2)
    year = int(updated_date[0])
    print(year)
    month = int(updated_date[1])
    day = int(updated_date[2])

    customer = Customer.query.filter_by(id=id_to_update).first()
    customer.name = updated_name
    customer.dob = datetime.date(year, month, day)
    customer.updated_at = datetime.datetime.now()
    db.session.commit()
    return jsonify(updated_customer_data)

# Delete a customer
@app.route('/customers', methods=['DELETE'])    
@token_required
def delete_customer():
    id_to_delete = int(request.args.get('delete_id', None))
    
    Customer.query.filter_by(id=id_to_delete).delete()
    db.session.commit()
    return jsonify({'deleted id': id_to_delete})

# List the n youngest customers ordered by date of birth
@app.route('/customers/youngest', methods=['GET'])
@token_required
def get_youngest_customers():
    n = int(request.args.get('n', None))
    customers_list = []
    customers = Customer.query.all()
    for customer in customers:
        current_customer = {}
        current_customer['id'] = customer.id
        current_customer['name'] = customer.name
        current_customer['dob'] = customer.dob
        current_customer['updated_at'] = customer.updated_at
        customers_list.append(current_customer)
    sorted_customers_list = sorted(customers_list, key = lambda i: i['dob'])
    youngest_customers_list = sorted_customers_list[:n]
    return jsonify(youngest_customers_list) 

if __name__ == '__main__':
    app.debug=True
    app.run()

