
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy points balance stored on the server
points_balance = 1000

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/update_points', methods=['POST'])
def update_points():
    global points_balance
    try:
        # Extract the new points balance from the request data
        new_points = request.json.get('new_points')
        logging.info(f"Received request to update points to {new_points}")
        
        # Update the points balance on the server
        points_balance = new_points
        
        # Return a success message
        return jsonify({'message': 'Points balance updated successfully', 'new_balance': points_balance}), 200
    except Exception as e:
        logging.error(f"Error updating points: {str(e)}")
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)}), 500

@app.route('/get_points', methods=['GET'])
def get_points():
    global points_balance
    logging.info("Received request to get points balance")
    # Return the current points balance
    return jsonify({'points_balance': points_balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
