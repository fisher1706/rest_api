# https://www.youtube.com/watch?v=cMz7J7iFuK8&list=PLWQhUNXl0LnjBIaE72hq1RkDsbWWSgeUr&index=8

from flask import Flask
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from videoblog.config import Config
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from videoblog.schemas import VideoSchema, UserSchema, AuthSchema
import logging

app = Flask(__name__)
app.config.from_object(Config)
client = app.test_client()

engine = create_engine('sqlite://///home/oleg/PycharmProjects/rest_api/videoblog/db.sqlite')
session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)

jwt = JWTManager()

docs = FlaskApiSpec()

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='V1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    ),
    'APISPEC_SWAGER_URL': '/swager/'
})


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('/home/oleg/PycharmProjects/rest_api/videoblog/log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from .main.views import videos
from .users.views import users


app.register_blueprint(videos)
app.register_blueprint(users)

docs.init_app(app)
jwt.init_app(app)
