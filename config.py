import os
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

#--------------------------------------------------------------------------------------------------#

DEBUG = True

#--------------------------------------------------------------------------------------------------#


default = 'postgresql://postgres:root@localhost/web_app'

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default)
SQLALCHEMY_TEST_DATABASE_URI = os.getenv('DATABASE_TEST_URI', None)

print(SQLALCHEMY_DATABASE_URI)

if os.environ.get("STAGE", None) == "test":
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_TEST_DATABASE_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

#--------------------------------------------------------------------------------------------------#

ROWS_PER_PAGE = 10

#--------------------------------------------------------------------------------------------------#

JWT_SECRET_KEY = '25bnDG2yKyvb9HRUSrysFBkbVnFONH8J'

#--------------------------------------------------------------------------------------------------#

BASE_DIR = os.path.dirname(os.path.abspath(__file__))