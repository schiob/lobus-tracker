from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import make_response
from flask.ext.httpauth import HTTPBasicAuth
import json
import datetime

app = Flask(__name__)


trucks = {}
last_pos = {}
# ============== Authentication =================
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'hack_mty':
        return 'pumas'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# ============== Data reset ================
@app.route('/reset', methods=['GET'])
@auth.login_required
def reset():
    global trucks
    global last_pos
    trucks = {}
    last_pos = {}
    return jsonify({'response': '200'}), 201

# ============== Data input ================

@app.route('/truck', methods=['POST'])
@auth.login_required
def new_pos():
    global trucks
    global last_pos
    if not request.json:
        abort(400)
    timestamp = datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    truck = {
        'id': request.json['id'],
        'timestamp': timestamp.strftime('%H:%M:%S - %d/%b/%y'),
        'pos': request.json['pos'],
        'dir': 'none'
    }
    if truck['id'] not in trucks:
        trucks[truck['id']] = truck
        last_pos[truck['id']] = truck
    else:
        trucks[truck['id']] = truck

        if truck['pos'][1] < last_pos[truck['id']]['pos'][1]:
            # Arteaga to Saltillo
            trucks[truck['id']]['dir'] = 'Arteaga -> Saltillo'
        else:
            # Saltillo to Arteaga
            trucks[truck['id']]['dir'] = 'Saltillo -> Arteaga'
        last_pos[truck['id']] = truck

    return jsonify({'truck': truck}), 201

# ============ Data output =================

@app.route("/data")
def data():
    global trucks
    result = {'trucks': [trucks[x] for x in trucks.keys()]}
    #turn the results into valid JSON
    print(trucks)
    return jsonify(result)

@app.route('/')
def get_students():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
