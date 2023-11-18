<hr>

<h1>📍How to install: </h1>

<!-- POSTMAN -->
<details><summary><h2>📮Connect to Postman:</h2></summary><br/>

<h3><b>1.1</b> Import `Postman Collections`folder into Postman</h3>
<h3><b>1.2</b> Set the environment settings `Weather.postman_environment`</h3>
<h3><b>1.3</b> The `E_Shop_API.postman_collection` collection contains requests</h3>

<h3><b>1.4</b> In your terminal, enter the following command:</h3>

```
ssh -R 80:localhost:8000 serveo.net
```

<p>Copy the forwarding message:</p>
<code>Forwarding HTTP traffic from <b>https://your_host.serveo.net</b></code>

<h3><b>1.5</b> Also set localhost in Postman:</h3>

```
http://localhost:8000/
```

</details>
<!-- END POSTMAN -->

<!-- DOCKER -->
<details><summary><h2>🐳Connect to Docker Compose:</h2></summary><br/>

<h3>2.1 Create Your .env and set correct values:</h3>

```
echo "Creating .env file..."
cat <<EOL > .env
# Django configuration
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=1

# PostgreSQL (docker/local)
DB_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=weather_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD_1=lolpop88
POSTGRES_PASSWORD=example
DB_PORT=5432

# pgadmin container
PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=root

# OPENWEATHERMA
OPENWEATHERMAP_URL=http://api.openweathermap.org/data/2.5/forecast
# OPENWEATHERMA API key (test)
OPENWEATHERMAP_API_KEY=5b44ac6286917292ea1dc572affc3aff
EOL
```

<h3>2.2 UP Docker-compose:</h3>

```
docker-compose -f docker/docker-compose.yml up --build
```

<h3>2.3 Login to the container console:</h3>

```
docker exec -it django-container bash
```

<h3>2.3 Login to the container console:</h3>

```
python3 manage.py createsuperuser
```

<h3>2.4 Localhost Database Setup:</h3>
<i>Create a database on localhost:5050</i>

- Open localhost:5050 in your browser.
- Register the server.
- In the connection settings:
    - Host: postgres-container
    - Username: postgres
    - Password: your_password

</details>
<!-- END DOCKER -->


# Endpoints

## Authentication Endpoints

- **POST** `/api/token/`: Log in and receive a JWT token.
- **POST** `/api/token/refresh/`: Refresh the JWT token.

## User Management Endpoints

- **POST** `/api/create_user/`: Create a new user.
- **GET/PUT/DELETE** `/api/users/<user_id>/`: CRUD operations for a specific user.
- **GET** `/api/users/`: Retrieve a list of all users.

## Weather Endpoints

- **GET** `/api/weather/current/`: Get the current weather at your location.
- **GET** `/api/weather/search/`: Get the current weather for a specified location.
- **GET** `/api/weather/forecast/`: Get a 7-day weather forecast for a specified location.
- **GET** `/api/weather/current_forecast/`: Get a 7-day weather forecast for your current location.
