import os

##############
# User input #
##############

# Debug
DEBUG = True

# config to modify db directly / test SQLAlchemy model from python terminal
SQLALCHEMY_TRACK_MODIFICATIONS = False

############
# No input #
############

# AUTH0 domain
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']

# AUTH0 hash algorithm
ALGORITHMS = [os.environ['ALGORITHMS']]

# AUTH0 api audience
API_AUDIENCE = os.environ['API_AUDIENCE']

# JWT config
JWT_CASTING_ASSISTANT = os.environ['JWT_CASTING_ASSISTANT']
JWT_CASTING_DIRECTOR  = os.environ['JWT_CASTING_DIRECTOR']
JWT_EXECUTIVE_PRODUCER = os.environ['JWT_EXECUTIVE_PRODUCER']

# Database path
DATABASE_PATH = os.environ['DATABASE_URL']
if DATABASE_PATH.startswith("postgres://"):
    DATABASE_PATH = DATABASE_PATH.replace("postgres://", "postgresql://", 1)