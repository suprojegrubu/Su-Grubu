from flask import Flask, render_template, request, jsonify
import time
import os

app = Flask(__name__)

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

@app.route("/track-user")
def track_user():
    ip = request.remote_addr
    active_users[ip] = time.time()
    return "", 204


@app.route("/stats")
def stats():
    now = time.time()

    for ip in list(active_users.keys()):
        if now - active_users[ip] > 30:
            del active_users[ip]

    return jsonify({
        "online": len(active_users)
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
