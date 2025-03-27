import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.sqlite_data_manager import SQLiteDataManager

load_dotenv(dotenv_path='config/.env')
API_KEY = os.getenv('API_KEY')
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte secret key
# Define the SQLite file path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'moviwebapp.sqlite')
db_file_name = f'sqlite:///{db_path}'

# Initialize the SQLiteDataManager with the app and db_file_name
data_manager = SQLiteDataManager(app, db_file_name)



@app.route('/')
def home_page():
    # Fetch top 5 movies based on rating
    movies = data_manager.best_movies()
    return render_template("home.html", movies=movies)

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)

@app.route('/users/<user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)  # Fetch movies for a specific user
    return render_template("user_movies.html", movies=movies, user_id=user_id)


@app.route('/add_user',methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get the username from the form
        username = request.form.get('user_name')
        if username:
            user = data_manager.add_user(username)
            if user is None:  # Either user already exists or database error
                flash(f"User '{username}' already exists or an error occurred. Please try again.", "error")
                return redirect(url_for('add_user'))

            flash(f"User '{username}' added successfully!", "success")
            return redirect(url_for('list_users'))  # Redirect to users list
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        # Get the movie name from the form
        movie_name = request.form['movie_name']

        # Build the full URL to fetch movie details
        movie_url = f"{URL}{movie_name}"

        # Fetch movie details from OMDb API
        response = requests.get(movie_url)
        movie_data = response.json()

        try:
            # Check if the movie data is valid
            if movie_data['Response'] == 'True':
                # Extract relevant movie details
                movie_title = movie_data.get('Title')
                movie_year = int(movie_data.get('Year'))
                movie_director = movie_data.get('Director')
                movie_rating = float(movie_data.get('imdbRating'))
                movie_poster = movie_data.get('Poster')

                # Use the data manager to add the movie to the database
                movie = data_manager.add_movie(
                    user_id=user_id,
                    movie_name=movie_title,
                    movie_director=movie_director,
                    movie_year=movie_year,
                    movie_rating=movie_rating,
                    movie_poster=movie_poster
                )
                if movie is None:
                    # Either movie already exists or database error
                    flash(f"Movie'{movie_name}' already exists or an error occurred. Please try again.")

                flash('Movie added successfully!', 'success')
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                flash('Movie not found or invalid data!', 'error')
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except requests.exceptions.RequestException as req_err:
            print(f"Error occurred while making the request: {req_err}")

        except Exception as err:
            print(f"An unexpected error occurred: {err}")

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>',methods=['GET', 'POST'] )
def update_movie(user_id,movie_id ):

    movie = data_manager.get_movie_by_id(movie_id)  # Fetch movies for a specific user

    if not movie:
        flash("Movie not found!", "error")
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        # Get updated details from the form
        movie_name = request.form.get('movie_name')
        movie_director = request.form.get('movie_director')
        movie_year = int(request.form.get('movie_year'))
        movie_rating = float(request.form.get('movie_rating'))
        data_manager.update_movie(user_id, movie_id, movie_name, movie_director, movie_year, movie_rating)
        flash(f"Movie updated successfully!", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user_id=user_id, movie=movie)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    flash(f"Movie deleted successfully!", "success")
    return redirect(url_for('user_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(505)
def internal_server_error(e):
    return render_template('505.html'), 505

if __name__ == '__main__':
    app.run(debug=True)
