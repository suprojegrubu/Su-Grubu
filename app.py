from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    email = request.form['email']
    message = request.form.get('message', '')

    new_applicant = Applicant(name=name, email=email, message=message)
    db.session.add(new_applicant)
    db.session.commit()

    return redirect('/') 

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


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
