from flask import Flask, render_template, request, redirect, url_for
from CarModel import db, Car ## Importing database and Car model from CarModel.py

app = Flask(__name__)


host = 'localhost'
port = '5432'
user = 'postgres'
password = 'Eleniko123'
database = 'flask'

app.secret_key = 'SecretApp' ## Secret key for session security

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) ## Initialize the database with the Flask app

@app.route('/')
def index():
    all_data = Car.query.all()
    return render_template('index.html', cars=all_data)



@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        car_id = request.form['id']  ## Get car ID from form submission
        car = Car.query.get(car_id)  ## Find the car in the database by ID

        if car: ## If exists, update these details
            car.manufacturer = request.form['manufacturer']
            car.model = request.form['model']
            car.instock = request.form['instock']
            car.price = request.form['price']

            db.session.commit() ## Commit changes to the database

        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
