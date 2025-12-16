from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time, os

app = Flask(__name__)
CORS(app)

active_users = {}

@app.route("/track-user", methods=["POST"])
def track_user():
    data = request.get_json()
    uid = data.get("id")
    if uid:
        active_users[uid] = time.time()
    return "", 204

@app.route("/stats")
def stats():
    now = time.time()
    TIMEOUT = 5
    
    for uid in list(active_users.keys()):
        if now - active_users[uid] > TIMEOUT:
            del active_users[uid]

    return jsonify({"online": len(active_users)})


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/siir', methods=['POST', 'GET'])
def siir():
    return render_template('page2.html')


@app.route('/hikaye', methods=['POST', 'GET'])
def hikaye():
    return render_template('page3.html')


@app.route('/kaynakca', methods=['POST', 'GET'])
def kaynakca():
    return render_template('page4.html')


@app.route('/ilginc-gercekler', methods=['POST', 'GET'])
def ilginc_gercekler():
    return render_template('page5.html')


@app.route('/ilginc-su-hayvanlari', methods=['POST', 'GET'])
def ilginc_su_hayvanlari():
    return render_template('page6.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
