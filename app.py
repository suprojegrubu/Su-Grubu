from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/moreabout', methods=['POST'])
def moreabout():
    return render_template('page2.html')


@app.route('/', methods=['POST'])
def gotoindex():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
