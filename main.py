from flask import Flask, render_template
from bus_mapper import *
import time

app = Flask(__name__)


@app.route('/')
def home():
    render_bus_locations('templates/index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
