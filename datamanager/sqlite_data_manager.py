from .data_manager_interface import DataManagerInterface
from .data_models import User, Movie, db


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app, db_file_name):
        self.app = app
        self.db_file_name = db_file_name

        # Flask app config for SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = db_file_name
        print(f"SQLAlchemy URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"Database file being used: {self.db_file_name}")

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
            print(f"Users found using ORM: {users}")
        return users

    def get_user_movies(self, user_id):
        # Query to fetch movies for a specific user
        with self.app.app_context():
            movies = Movie.query.filter_by(user_id=user_id).all()
            print(f"Movies found for user {user_id}: {movies}")  # Debug print to check the results
        return movies

    def add_test_data(self):
        with self.app.app_context():
            # Check if test user exists
            test_user = User.query.filter_by(user_name='test_user').first()
            if not test_user:
                # Add test user
                new_user = User(user_name='test_user')
                self.db.session.add(new_user)
                self.db.session.commit()
                print("Test user added")
