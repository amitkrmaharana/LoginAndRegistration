import jwt
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config

bp = Blueprint('bp', __name__)
from models import *


@bp.route('/register', methods=['POST', 'GET'])
def register_user():
    """
    This method registers a new user to the database
    :return: a new registration
    """
    try:
        if request.method == 'POST':
            data = request.json
            user = Users(id=data.get('id'), first_name=data.get('first_name'), last_name=data.get('last_name'),
                         email=data.get('email'),
                         contact=data.get('contact'), username=data.get('username'),
                         password=generate_password_hash(data.get('password')))
            database.session.add(user)
            database.session.commit()
            username = data.get('username')
            user = Users.query.filter(Users.username == username).first()
            if not user:
                return make_response("Username not registered", 401)
            else:
                token = jwt.encode({'username': username}, Config.SECRET_KEY)
                verify = redirect(url_for('bp.is_verify', token=token, username=username))
                if verify:
                    return make_response("Registration successful", 200)
                return make_response("Registration unsuccessful", 401)
        else:
            return make_response("Registration unsuccessful, did not hit POST method", 401)
    except Exception as e:
        logger.exception(e)
        return make_response("Username and id already taken in database", 401)


@bp.route('/login', methods=['POST'])
def login_user():
    """
    This method makes a login if a valid username or password is provided
    :return: returns successful if logged in and unsuccessful if not logged in
    """
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = Users.query.filter(Users.username == username).first()
        if not user or not check_password_hash(user.password, password):
            return make_response("Bad username or password", 401)
        else:
            token = jwt.encode({'username': username}, Config.SECRET_KEY)
            verify = redirect(url_for('bp.is_verify', token=token, username=username))
            if verify:
                return make_response("Login successful", 200)
            return make_response("Login unsuccessful", 401)
    except Exception as e:
        logger.exception(e)
        return make_response("Bad request", 401)


@bp.route('/verify/<token>/<username>', methods=['GET'])
def is_verify(token=None, username=None):
    """
    This route decodes a given token and checks if the token is valid for a username or not
    :param token: token generated
    :param username: username given
    :return: boolean
    """
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
        if data.get('username') == username:
            return True
        return False
    except Exception as e:
        logger.exception(e)
        return make_response("Token not available", 401)
