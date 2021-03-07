# REST API - check basic car makes and models existence in database. Add, rate, delete and view most rated cars.
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
Install requirements:
```
pip install -r requirements.txt
```

If you are not using Docker to run project locally you can also run it by typing in terminal:
```
py manage.py runserver --settings car_api.settings_local
```
