import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from config import DATABASE_PATH, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_CASTING_ASSISTANT, JWT_CASTING_DIRECTOR, JWT_EXECUTIVE_PRODUCER


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            

        # test variable setup
        self.auth_assistant = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + JWT_CASTING_ASSISTANT
        }

        self.auth_director = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + JWT_CASTING_DIRECTOR
        }

        self.auth_producer = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + JWT_EXECUTIVE_PRODUCER
        }

        self.n_actor = {
            "name": "Harucha",
            "age": "26",
            "gender": "Female"
        }

        self.n_movie = {
            "title": "Detective Conan Movie 26",
            "release_date": "2023-05-05"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_actors_success(self):
        res = self.client().get("/actors", headers=self.auth_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue("actors" in data)

    def test_get_actors_fail(self):
        res = self.client().get("/actors") # no auth
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_movies_success(self):
        res = self.client().get("/movies", headers=self.auth_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue("movies" in data)

    def test_get_movies_fail(self):
        res = self.client().get("/movies") # no auth
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_add_delete_actors_success(self):
        total_actor = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])
        res = self.client().post("/actors", json=self.n_actor, headers=self.auth_director)
        total_actor_after_insert = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])
        data = json.loads(res.data)

        self.assertTrue(total_actor_after_insert - total_actor == 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

        # delete dummy insert
        insert_id = data["actors"][0]["id"]
        res = self.client().delete("/actors/" + str(insert_id), headers=self.auth_director)
        data = json.loads(res.data)
        total_actor_after_delete = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])

        self.assertEqual(total_actor, total_actor_after_delete)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], insert_id)

    def test_add_actors_fail(self):
        dummy_actor = {
            "name": self.n_actor["name"],
            "age": self.n_actor["age"],
        }  # lack of gender field
        res = self.client().post("/actors", json=dummy_actor, headers=self.auth_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_delete_actor_fail(self):
        res = self.client().delete("/actors/1000000", headers=self.auth_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_add_delete_movies_success(self):
        total_movie = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])
        res = self.client().post("/movies", json=self.n_movie, headers=self.auth_producer)
        total_movie_after_insert = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])
        data = json.loads(res.data)

        self.assertTrue(total_movie_after_insert - total_movie == 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

        # delete dummy insert
        insert_id = data["movies"][0]["id"]
        res = self.client().delete("/movies/" + str(insert_id), headers=self.auth_producer)
        data = json.loads(res.data)
        total_movie_after_delete = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])

        self.assertEqual(total_movie, total_movie_after_delete)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], insert_id)

    def test_add_movies_fail(self):
        dummy_movie = {
            "title": self.n_movie["title"],
        }  # lack of release_date field
        res = self.client().post("/movies", json=dummy_movie, headers=self.auth_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_delete_movie_fail(self):
        res = self.client().delete("/movies/1000000", headers=self.auth_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_add_patch_delete_actors_success(self):
        # add actor
        total_actor = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])
        res = self.client().post("/actors", json=self.n_actor, headers=self.auth_director)
        total_actor_after_insert = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])
        data = json.loads(res.data)

        self.assertTrue(total_actor_after_insert - total_actor == 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

        # patch actor
        insert_id = data["actors"][0]["id"]
        res = self.client().patch("/actors/" + str(insert_id), json=self.n_actor, headers=self.auth_director)
        total_actor_after_insert = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])
        data = json.loads(res.data)

        self.assertTrue(total_actor_after_insert - total_actor == 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

        # delete dummy insert
        res = self.client().delete("/actors/" + str(insert_id), headers=self.auth_director)
        data = json.loads(res.data)
        total_actor_after_delete = len(json.loads(self.client().get("/actors", headers=self.auth_director).data)["actors"])

        self.assertEqual(total_actor, total_actor_after_delete)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], insert_id)

    def test_add_patch_delete_movies_success(self):
        # add movie
        total_movie = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])
        res = self.client().post("/movies", json=self.n_movie, headers=self.auth_producer)
        total_movie_after_insert = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])
        data = json.loads(res.data)

        self.assertTrue(total_movie_after_insert - total_movie == 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

        # patch movie
        insert_id = data["movies"][0]["id"]
        res = self.client().patch("/movies/" + str(insert_id), json=self.n_movie, headers=self.auth_producer)
        total_movie_after_insert = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])
        data = json.loads(res.data)

        self.assertTrue(total_movie_after_insert - total_movie == 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

        # delete dummy insert
        res = self.client().delete("/movies/" + str(insert_id), headers=self.auth_producer)
        data = json.loads(res.data)
        total_movie_after_delete = len(json.loads(self.client().get("/movies", headers=self.auth_producer).data)["movies"])

        self.assertEqual(total_movie, total_movie_after_delete)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], insert_id)

    def test_patch_actor_fail(self):
        res = self.client().patch("/actors/1000000", json=self.n_actor, headers=self.auth_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_patch_movie_fail(self):
        res = self.client().patch("/movies/1000000", json=self.n_movie, headers=self.auth_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
