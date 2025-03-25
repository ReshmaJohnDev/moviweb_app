import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.sqlite_data_manager import SQLiteDataManager

# Initialize Flask app
app = Flask(__name__)

# Define the SQLite file path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'moviwebapp.sqlite')
db_file_name = f'sqlite:///{db_path}'

# Initialize the SQLiteDataManager with the app and db_file_name
data_manager = SQLiteDataManager(app, db_file_name)

@app.route('/add_test_data')
def add_test_data_route():
    data_manager.add_test_data()
    return "Test data added successfully!", 200

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/users')
def list_user():
    pass

@app.route('/users/<user_id>')
def user_movies(user_id):
    pass

@app.route('/add_user')
def add_user():
    pass

@app.route('/users/<user_id>/add_movie')
def add_movie():
    pass

@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie():
    pass

@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    pass


if __name__ == '__main__':
    app.run(debug=True)
