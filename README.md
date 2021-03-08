# Basic Django Rest API - check basic car makes and models existence in database. Add, rate, delete and view most rated cars.
API is interacting with an external API https://vpic.nhtsa.dot.gov/api/ for car existence validation.

Available online: http://car-django-api.herokuapp.com/cars/

# Endpoints: 
(more detailed description to the endpoints with described data structure for POST/DELETE requests can be found in 'endpoints.txt')

GET /cars/

POST /cars/

DELETE /cars/{ id }/

POST /rate/

  GET /popular/

You can interact with the API only programmatically. This means you have to use tools like POSTMAN, or send requests programmatically to the relative endpoints.

Interracting with API does not require authentication.

# Run project on local machine - project is dockerized with use of docer-compose.

To run project on Docker on local machine: 

1. Clone project to local machine
2. Create a file '.env' in a project root directory and set your environment variables. 
You can find an example of a file 'env.template'.
3. Run in a terminal:
```
docker-compose up
```

# Dummy data:

To load dummy-data:
```
py manage.py loaddata test_car_data.json
```

# Testing and logging issues:

All provided requirements are covered with testing. 

You can run tests:
```py manage.py tests```

# Logging issues:

Any issues when interracting with API are printed out in the terminal.

# Development
If you do not use Docker, you can also run project after some basic project setup.
## Setup
Create and activate a virtual environment (Python3) using your preferred method. This functionality is built into Python, if you do not have a preference.

From the command line, type:
```
git clone https://github.com/klimuntowskirafal/car_api
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata test_car_data.json
python manage.py runserver --settings car_api.settings_local
```

Open your browser to http://localhost:8000/cars/ and you should see the browsable version of the API.
