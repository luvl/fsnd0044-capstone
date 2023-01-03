import sys
import traceback

from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import rollback_db, close_db, setup_db, Movie, Actor
from exceptions import ACTOR_EXCEPTION, MOVIE_EXCEPTION, AUTH_ERROR
from auth import requires_auth
from config import DEBUG
from util import Gender


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    # ROUTES    
    '''
        GET /
            healcheck application
            authorize: Casting Assistant, Casting Director and Executive Producer
    '''


    @app.route('/', methods=['POST', 'GET'])
    def get_healthcheck():
        return jsonify("Healthy")


    '''
        GET /actors
            public endpoint
            authorize: Casting Assistant, Casting Director and Executive Producer
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
    '''


    @app.route("/actors", methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(payload):
        err = False
        try:
            actors_db = Actor.query.all()
            actors = [actor.format() for actor in actors_db]
            res = {
                "success": True,
                "actors": actors,
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            raise ACTOR_EXCEPTION
        finally:
            if not err:
                return jsonify(res), 200
            else:
                abort(500)


    '''
        GET /movies
            public endpoint
            authorize: Casting Assistant, Casting Director and Executive Producer
        returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
    '''


    @app.route("/movies", methods=["GET"])
    @requires_auth('get:actors')
    def get_movies(payload):
        err = False
        try:
            movies_db = Movie.query.all()
            movies = [movie.format() for movie in movies_db]
            res = {
                "success": True,
                "movies": movies,
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            raise ACTOR_EXCEPTION
        finally:
            if not err:
                return jsonify(res), 200
            else:
                abort(500)


    '''
        DELETE /actors/<id>
            where <id> is the existing actor id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission for Casting Director and Executive Producer
            authorize: Casting Director and Executive Producer
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    '''


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        err = False
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        try:
            actor.delete()
            res = {
                "success": True,
                "delete": actor.id
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            rollback_db()
            raise ACTOR_EXCEPTION
        finally:
            close_db()
            if err:
                return abort(422)
            else:
                return jsonify(res), 200


    '''
        DELETE /movies/<id>
            where <id> is the existing movie id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission for Executive Producer
            authorize: Executive Producer
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    '''


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        err = False
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        try:
            movie.delete()
            res = {
                "success": True,
                "delete": movie.id
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            rollback_db()
            raise MOVIE_EXCEPTION
        finally:
            close_db()
            if err:
                return abort(422)
            else:
                return jsonify(res), 200


    '''
        POST /actors
            it should create a new row in the actors table
            it should require the 'post:actors' permission permission for Casting Director and Executive Producer
            authorize: Casting Director and Executive Producer
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
    '''


    @app.route("/actors", methods=["POST"])
    @requires_auth('post:actors')
    def add_actors(payload):
        err = False
        data = request.json
        if 'name' not in data or 'age' not in data or 'gender' not in data:
            abort(422)

        try:
            new_actor = Actor(
                name=data.get("name"),
                age=data.get("age"),
                gender=Gender[data.get("gender").upper()].value,
            )
            new_actor.insert()
            actor = [new_actor.format()]
            res = {
                "success": True,
                "actors": actor
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            rollback_db()
            raise ACTOR_EXCEPTION
        finally:
            close_db()
            if not err:
                return jsonify(res), 200
            else:
                abort(422)


    '''
        POST /movies
            it should create a new row in the movies table
            it should require the 'post:movies' permission permission for Executive Producer
            authorize: Executive Producer
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
    '''


    @app.route("/movies", methods=["POST"])
    @requires_auth('post:movies')
    def add_movies(payload):
        err = False
        data = request.json
        if 'title' not in data or 'release_date' not in data:
            abort(422)

        try:
            new_movie = Movie(
                title=data.get("title"),
                release_date=data.get("release_date"),
            )
            new_movie.insert()
            movie = [new_movie.format()]
            res = {
                "success": True,
                "movies": movie
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            rollback_db()
            raise MOVIE_EXCEPTION
        finally:
            close_db()
            if not err:
                return jsonify(res), 200
            else:
                abort(422)


    '''
        PATCH /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actors' permission for Casting Director and Executive Producer
            authorize: Casting Director and Executive Producer
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
    '''


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, actor_id):
        err = False
        data = request.get_json()
        if 'name' not in data or 'age' not in data or 'gender' not in data:
            abort(422)

        actor_db = Actor.query.get(actor_id)
        if not actor_db:
            abort(404)
        if 'name' in data:
            actor_db.name = data.get('name')
        if 'age' in data:
            actor_db.age = data.get('age')
        if 'gender' in data:
            actor_db.gender = Gender[data.get('gender').upper()].value

        try:
            actor_db.update()
            actor = [actor_db.format()]
            res = {
                "success": True,
                "actors": actor
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            rollback_db()
            raise ACTOR_EXCEPTION
        finally:
            close_db()
            if not err:
                return jsonify(res), 200
            else:
                abort(422)


    '''
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission for Casting Director and Executive Producer
            authorize: Casting Director and Executive Producer
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
    '''


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload, movie_id):
        err = False
        data = request.get_json()
        if 'title' not in data or 'release_date' not in data:
            abort(422)

        movie_db = Movie.query.get(movie_id)
        if not movie_db:
            abort(404)
        if 'title' in data:
            movie_db.title = data.get('title')
        if 'release_date' in data:
            movie_db.release_date = data.get('release_date')

        try:
            movie_db.update()
            movie = [movie_db.format()]
            res = {
                "success": True,
                "movies": movie
            }
        except:
            err = True
            print(sys.exc_info())
            print(traceback.format_exc())
            rollback_db()
            raise MOVIE_EXCEPTION
        finally:
            close_db()
            if not err:
                return jsonify(res), 200
            else:
                abort(422)


    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AUTH_ERROR)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

# FLASK-SETUP This code should be at the bottom of all your files.
if __name__ == '__main__':
    app.run(port=3000, debug=DEBUG)