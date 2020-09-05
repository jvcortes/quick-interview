# quick-interview
REST API made in Django with Django REST Framework using DRF's APIView class.

## Requirements
* Python 3.6 or higher
* Django 3.1 or higher
* Django REST Framework 3.11 or higher
* `djangorestframework-simplejwt` 4.4.0
* `djangorestframework-csv` 2.1.0
* sqlite3

## Instructions

* Clone this repository
```console
git clone https://www.github.com/jvcortes/quick-interview
```

* Create a virtual environment inside the project's folder
```console
cd quick-interview
python3 -m venv .
```

* Install dependencies from `requirements.txt`
```console
python3 -m pip install -r requirements.txt
```

* Make migrations and migrate
```console
python3 manage.py makemigrations && python3 manage.py migrate
```

* Start the development server
```console
python3 manage.py runserver
```

## Content

The application contains the following endpoints:
* `/api/v1/registration/` (POST): User registration, accepts the following fields:
	* `email`: user email
	* `password`: user password
	* `document`: user identification document
* `/api/token/` (POST): See user's current access JWT and long duration JWT:
	* `email`: user email
	* `password`: user password
* `/api/token/refresh` (POST): Get access token through user's long duration JWT
	* `email`: user email
	* `password`: user password
	* `refresh`: user long duration JWT

### Protected endpoints

To access these endpoints, an `Authorization` header with a `Bearer <access_token>` value is required.

* `/api/v1/clients/` (all methods): CRUD operations for clients, see `api/models.py`, `Client` class for more details
* `/api/v1/clients/as_csv/` (GET): CSV export for all `Client` instances.
* `/api/v1/clients/import/` (PUT): CSV import for `Client` instances creation through multipart file upload.
* `/api/v1/products/` (all methods): CRUD operations for products, see `api/models.py`, `Product` class for more details
* `/api/v1/bills/` (all methods): CRUD operations for client bills, see `api/models.py`, `Bill` class for more details

