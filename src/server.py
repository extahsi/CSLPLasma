from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points_balance = db.Column(db.Integer, nullable=False)

    def __init__(self, points_balance):
        self.points_balance = points_balance

@app.before_first_request
def create_tables():
    db.create_all()
    if not UserPoints.query.first():
        db.session.add(UserPoints(points_balance=1000))  # Initial balance
        db.session.commit()

@app.route('/update_points', methods=['POST'])
def update_points():
    try:
        # Extract the new points balance from the request data
        new_points = request.json.get('new_points')
        
        # Update the points balance on the server
        user_points = UserPoints.query.first()
        user_points.points_balance = new_points
        db.session.commit()
        
        # Return a success message
        return jsonify({'message': 'Points balance updated successfully', 'new_balance': user_points.points_balance}), 200
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

@app.route('/get_points', methods=['GET'])
def get_points():
    # Return the current points balance
    user_points = UserPoints.query.first()
    return jsonify({'points_balance': user_points.points_balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
