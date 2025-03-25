from .data_manager_interface import DataManagerInterface
from .data_models import User, Movie, db


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app, db_file_name):
        self.app = app
        self.db_file_name = db_file_name

        # Flask app config for SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = db_file_name

        # Initialize SQLAlchemy with the app
        self.db = db
        db.init_app(app)

        # Create the tables if they don't already exist
        with app.app_context():
            db.create_all()

    def get_all_users(self):
        # Query to fetch all users
        with self.app.app_context():
            users = User.query.all()  # Using ORM query
        return users

    def get_user_movies(self, user_id):
        # Query to fetch movies for a specific user
        with self.app.app_context():
            movies = Movie.query.filter_by(user_id = user_id).all()
        return movies

    def add_user(self, user_name):
        with self.app.app_context():
            new_user = User(
                user_name = user_name,
            )
            db.session.add(new_user)
            db.session.commit()

    def add_movie(self, user_id, movie_name, movie_director, movie_year, movie_rating):
        with self.app.app_context():
            new_movie = Movie(
                movie_name = movie_name,
                movie_director = movie_director,
                movie_year = movie_year,
                movie_rating = movie_rating,
                user_id = user_id
            )
            db.session.add(new_movie)
            db.session.commit()

    def update_movie(self, user_id, movie_id):
        pass

    def delete_movie(self, user_id, movie_id):
        pass


