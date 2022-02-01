from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)
index_blueprint = Blueprint('user_index', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        print('inside self')
        post_data = request.get_json(); print(request)
        print('This is post data: ',post_data)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                print('added user')
                db.session.commit()
                print('committed table')
                # generate the auth token
                print(str(user))
                print(str(user.id))
                auth_token = user.encode_auth_token(user.id)
                print(str(auth_token))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                print(str(make_response))
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)


class IndexAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        data = {}
        i = 0
        users = User.query.all()

        for user in users:
            data[i] = {
                'admin': user.admin,
                'email': user.email,
                'id': user.id,
                'registered_on': user.registered_on
            }
            i += 1

        return make_response(jsonify(data)), 201


# define the API resources
index_view = IndexAPI.as_view('index_api')

# add Rules for API Endpoints
index_blueprint.add_url_rule(
    '/users/index',
    view_func=index_view,
    methods=['GET']
)