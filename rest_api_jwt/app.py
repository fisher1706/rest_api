from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from rest_api_jwt.config import Config


app = Flask(__name__)
client = app.test_client()
app.config.from_object(Config)

engine = create_engine('sqlite://///home/oleg/PycharmProjects/rest_api/rest_api_jwt/jwt.sqlite')
session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

from rest_api_jwt.models import *
Base.metadata.create_all(bind=engine)

jwt = JWTManager(app)


@app.route('/tutorials', methods=['GET'])
@jwt_required()
def get_list():
    user_id = get_jwt_identity()
    videos = Video.query.filter(Video.user_id == user_id)

    serialized = []
    for video in videos:
        serialized.append(
            {
                'id': video.id,
                'user_id': video.user_id,
                'name': video.name,
                'descrpition': video.description
            }
        )

    return jsonify(serialized)


@app.route('/tutorials', methods=['POST'])
@jwt_required()
def update_list():
    user_id = get_jwt_identity()
    new_one = Video(user_id=user_id, **request.json)

    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'user_id': new_one.user_id,
        'name': new_one.name,
        'descrpition': new_one.description
    }

    return jsonify(serialized)


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required()
def update_tutorial(tutorial_id):
    user_id = get_jwt_identity()
    item = Video.query.filter(Video.id == tutorial_id,
                              Video.user_id == user_id).first()
    params = request.json
    print(f'\nparams: {params}')

    if not item:
        return {'message': 'No tutorials with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()

    serialized = {
        'id': item.id,
        'user_id': item.user_id,
        'name': item.name,
        'descrpition': item.description
        }

    return serialized


@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required()
def delete_tutorial(tutorial_id):
    user_id = get_jwt_identity()
    item = Video.query.filter(Video.id == tutorial_id,
                              Video.user_id == user_id).first()

    if not item:
        return {'message': 'No tutorials with this id'}, 400

    session.delete(item)
    session.commit()

    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    print(f'\nuser.password: {user.password}')
    session.add(user)
    session.commit()
    token = user.get_token()

    return {'access_token': token}, 200


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    print(f'\ntoken: {token}')

    return {'access_token': token}


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)
