MovieWeb App
MovieWeb App is a Flask-based web application that allows users to manage their movie collections.
It includes functionalities such as adding, updating, and deleting movies, as well as viewing popular movies and their details.
The app uses SQLite as a backend database to store user and movie.

Features
User Management:
Add new users.
View list of users.
View each user's movie collection.

Movie Management:
Add movies to a user's collection.
Update movie details (title, director, year, rating).
Delete movies from a user's collection.

Top-rated Movies:
Display the top 5 rated movies based on IMDb ratings.
Before you start, ensure you have the following dependencies installed:
Python 3.8+ (or a compatible version)

Requirements

Python 3.8+ (or a compatible version)
Flask
Flask-SQLAlchemy
Requests
dotenv

Setup
git clone https://github.com/ReshmaJohnDev/moviweb_app.git
cd movieweb-app

Install the necessary dependencies:
pip install -r requirements.txt

Set up the .env file for storing the API key (OMDb API):
Create a file named .env in the config directory.
Add your OMDb API key to the file:
API_KEY=your_omdb_api_key_here

Run the Flask app:
python app.py

Routes
/: Home page displaying the top 5 rated movies.
/users: View all users.
/users/<user_id>: View movies of a specific user.
/add_user: Add a new user.
/users/<user_id>/add_movie: Add a movie to a user's collection.
/users/<user_id>/update_movie/<movie_id>: Update movie details.
/users/<user_id>/delete_movie/<movie_id>: Delete a movie from a user's collection.

Database Structure
The application uses SQLAlchemy with SQLite as the database backend. There are two main models:
User: Represents a user with a unique user_name.
Movie: Represents a movie in a user's collection with attributes like
movie_name, movie_director, movie_year, movie_rating, and movie_poster. Each movie is associated with a specific user.

Error Handling
The application includes custom error pages for:

404: Page not found.
505: Internal server error.






