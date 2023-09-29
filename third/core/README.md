# Challenge Payments API

## Getting Started Locally

To run this project locally, you will need to have the following dependencies installed:

- Django==3.1
- djangorestframework==3.11.1
- drf-yasg==1.20.0

You can install these dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Database Migrations
Before you can start the development server, you need to apply the database migrations. Run the following commands to apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Development Server
Once you have installed the dependencies, you can start the development server by running the following command:
```bash
python manage.py runserver
```
The API will be available at http://localhost:8000/.

You can find the complete API documentation at the following link:

[API Documentation](http://localhost:8000/swagger/)