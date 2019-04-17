from flask import Flask, render_template, jsonify
from bus_mapper import *
import time, os

app = Flask(__name__)

# Get our webpage
@app.route('/')
def home():
    return render_template('index.html')

# Get bus locations
@app.route('/busses')
def markers():
    data = get_bus_locations()
    return jsonify({"data": data})

# Get the paths to draww on the map
@app.route('/paths')
def paths():
    data = get_bus_paths()
    return jsonify({"data" : data})
        
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
