from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
db = SQLAlchemy(app)

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/update_points', methods=['POST'])
def update_points():
    try:
        new_points = request.json.get('new_points')
        points = Points.query.first()
        if points is None:
            points = Points(balance=new_points)
            db.session.add(points)
        else:
            points.balance = new_points
        db.session.commit()
        return jsonify({'message': 'Points balance updated successfully', 'new_balance': points.balance}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_points', methods=['GET'])
def get_points():
    points = Points.query.first()
    return jsonify({'points_balance': points.balance if points else 0}), 200

if __name__ == '__main__':
    app.run(debug=True)
