# Casting Agency API Backend

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Casting Agency API backend is an application that manages movies and actors whose attributes as following:

Models:
- Movies with attributes title and release date
- Actors with attributes name, age and gender

Roles:
 - Casting Assistant: Can view actors and movies
 - Casting Director: All permissions a Casting Assistant has, add or delete an actor from the database and modify actors or movies
 - Executive Producer: All permissions a Casting Director has and add or delete a movie from the database

## Getting Started

### Installing Dependencies

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.  


4. **Key Dependencies**  
[Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.  
[SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.   
[Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.   


## Configuration

### Authentication
JWTs are provided within setup.sh for Casting Assistant, Casting Director and Executive Producer, valid until 2023-04-01

### Application configure
Refer to config.py to setup debug mode

### Test configure
Run following script to run unittest
```bash
python test_app.py
```
Postman API are exported for API testing, import the API collection file "FSND0044-Final-Project-Test.postman_collection.json" in Postman for random testing


### Deployment
Refer to following production endpoint which is deployed with Heroku: T.B.D


# API Endpoint

**1.** `GET '/'`
* Get healthcheck of application
* Returns: "Healthy" which indicates apps is runniing


**2.** `GET '/actors'`
* Fetches a dictionary of actors
* Request Arguments: None
* Returns: An object with a following keys.
* success (bool): return status True for success, False for failure
* actors (dict): total actors fetched from database which is in following json format:
```json
{
  "name": "{the name of the actor}",
  "age": "{the age of the actor}",
  "gender": "{the gender of the actor}",
}
```


**3.** `GET '/movies'`
* Fetches a dictionary of movies
* Request Arguments: None
* Returns: An object with a following keys.
* success (bool): return status True for success, False for failure
* movies (dict): total movies fetched from database which is in following json format:
```json
{
  "title": "{the title of the movie}",
  "release_date": "{the release_date of the movie}",
}
```


**4.** `DELETE '/actors/<int:actor_id>'`
* Delete actor using a actor ID.
* Request Arguments: None
* Returns: An object with two keys as following
* success (bool): return status True for success, False for failure
* delete (int): delete actor_id


**5.** `DELETE '/movies/<int:movie_id>'`
* Delete movie using a movie ID.
* Request Arguments: None
* Returns: An object with two keys as following
* success (bool): return status True for success, False for failure
* delete (int): delete movie_id


**6.** `POST '/actors'`
* Add a new actor, which will require the actor name, age and gender
* Request Arguments: 
```json
{
  "name": "{the name of the actor}",
  "age": "{the age of the actor}",
  "gender": "{the gender of the actor}",
}
```
* Returns: An object with two keys as following
* success (bool): return status True for success, False for failure
* actors (dict): total actors added to database which is in following json format:
```json
{
  "name": "{the name of the actor}",
  "age": "{the age of the actor}",
  "gender": "{the gender of the actor}",
}
```


**7.** `POST '/movies'`
* Add a new movie, which will require the movie title and release date
* Request Arguments: 
```json
{
  "title": "{the title of the movie}",
  "release_date": "{the release_date of the movie}",
}
```
* Returns: An object with two keys as following
* success (bool): return status True for success, False for failure
* movies (dict): total movies added to database which is in following json format:
```json
{
  "title": "{the title of the movie}",
  "release_date": "{the release_date of the movie}",
}
```


**8.** `PATCH '/actors/<int:actor_id>'`
* Update a new actor, which will require the actor name, age and gender as well as actor id to update
* Request Arguments: actor id and json data as following
```json
{
  "name": "{the name of the actor}",
  "age": "{the age of the actor}",
  "gender": "{the gender of the actor}",
}
```
* Returns: An object with two keys as following
* success (bool): return status True for success, False for failure
* actors (dict): total actors added to database which is in following json format:
```json
{
  "name": "{the name of the actor}",
  "age": "{the age of the actor}",
  "gender": "{the gender of the actor}",
}
```


**9.** `PATCH '/movies/<int:movie_id>'`
* Update a new movie, which will require the movie title and release date as well as movie id to update
* Request Arguments: movie id and json data as following
```json
{
  "title": "{the title of the movie}",
  "release_date": "{the release_date of the movie}",
}
```
* Returns: An object with two keys as following
* success (bool): return status True for success, False for failure
* movies (dict): total movies added to database which is in following json format:
```json
{
  "title": "{the title of the movie}",
  "release_date": "{the release_date of the movie}",
}
```