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

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/users')
def list_user():
    users = data_manager.get_all_users()
    print(users)
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
