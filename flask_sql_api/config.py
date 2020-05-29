from env import SECRET_KEY, SQLALCHEMY_DATABASE_URI#    ---->Senisitive data like secret key and database url are stored in separate env.py file

class Config:

    # General Configuration
    TESTING=True
    SECRET_KEY=SECRET_KEY

    STATIC_FOLDER='static'
    TEMPLATES_FOLDER='templates'

    # Database Configuration
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
