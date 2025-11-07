from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/siir', methods=['POST'])
def siir():
    return render_template('page2.html')

@app.route('/hikaye', methods=['POST'])
def hikaye():
    return render_template('page3.html')

@app.route('/kaynakca', methods=['POST'])
def kaynakca():
    return render_template('page4.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
