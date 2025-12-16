from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import time, os, uuid

app = Flask(__name__)
CORS(app)

active_users = {}
TIMEOUT = 5

@app.route("/track-user", methods=["POST"])
def track_user():
    data = request.get_json()
    uid = data.get("id")
    if uid:
        active_users[uid] = time.time()
    return "", 204

VISITOR_FILE = "visitors.txt"

def get_unique_count():
    if not os.path.exists(VISITOR_FILE):
        return 0
    with open(VISITOR_FILE, "r") as f:
        return len(set(f.readlines()))

def save_visitor(visitor_id):
    with open(VISITOR_FILE, "a") as f:
        f.write(visitor_id + "\n")

def visitor_exists(visitor_id):
    if not os.path.exists(VISITOR_FILE):
        return False
    with open(VISITOR_FILE, "r") as f:
        return visitor_id in f.read()

@app.route("/stats")
def stats():
    now = time.time()

    for uid in list(active_users.keys()):
        if now - active_users[uid] > TIMEOUT:
            del active_users[uid]

    return jsonify({
        "online": len(active_users),
        "unique": get_unique_count()
    })
    
@app.route('/')
def index():
    visitor_id = request.cookies.get("visitor_id")

    if not visitor_id:
        visitor_id = str(uuid.uuid4())
        save_visitor(visitor_id)
    else:
        if not visitor_exists(visitor_id):
            save_visitor(visitor_id)

    response = make_response(render_template("index.html"))
    response.set_cookie(
        "visitor_id",
        visitor_id,
        max_age=60 * 60 * 24 * 365  
    )
    return response

@app.route('/siir', methods=["POST", "GET"])
def siir():
    return render_template('page2.html')

@app.route('/hikaye', methods=["POST", "GET"])
def hikaye():
    return render_template('page3.html')

@app.route('/kaynakca', methods=["POST", "GET"])
def kaynakca():
    return render_template('page4.html')

@app.route('/ilginc-gercekler', methods=["POST", "GET"])
def ilginc_gercekler():
    return render_template('page5.html')

@app.route('/ilginc-su-hayvanlari', methods=["POST", "GET"])
def ilginc_su_hayvanlari():
    return render_template('page6.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
