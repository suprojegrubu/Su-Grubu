from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time, os, requests, base64

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


@app.route("/stats")
def stats():
    now = time.time()

    for uid in list(active_users.keys()):
        if now - active_users[uid] > TIMEOUT:
            del active_users[uid]

    return jsonify({
        "online": len(active_users)
    })

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = "suprojegrubu/Su-Grubu"
FILE_PATH = "counter.txt"
BRANCH = "main"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def increment_total_visits():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    r = requests.get(url, headers=HEADERS)
    data = r.json()

    sha = data["sha"]
    current = int(
        base64.b64decode(data["content"]).decode().strip()
    )

    new_value = current + 1

    requests.put(
        url,
        headers=HEADERS,
        json={
            "message": "Ziyaret+1",
            "content": base64.b64encode(
                str(new_value).encode()
            ).decode(),
            "sha": sha,
            "branch": BRANCH
        }
    )

    return new_value

@app.route("/")
def index():
    total_visits = increment_total_visits()
    return render_template("index.html", total=total_visits)

@app.route("/siir")
def siir():
    return render_template("page2.html")

@app.route("/hikaye")
def hikaye():
    return render_template("page3.html")

@app.route("/kaynakca")
def kaynakca():
    return render_template("page4.html")

@app.route("/ilginc-gercekler")
def ilginc_gercekler():
    return render_template("page5.html")

@app.route("/ilginc-su-hayvanlari")
def ilginc_su_hayvanlari():
    return render_template("page6.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
