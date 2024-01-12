# Quiz Management System

The Quiz Management System is a Django web application designed for quiz app management.

## Features

- User registration with first name, last name, and username.
- CRUD operations on quizzes: Create, Read, Update, Delete.
- Admin can track scores.
- Students can take quizzes and evaluate their performance.

## Technologies Used

- Python
- Django
- PostgreSQL
- HTML
- CSS

## Getting Started

To run this project, follow these steps:

### Step 1 – Install Python and Django

Make sure you have Python and Django installed on your system. Check the current versions using the following commands:

```bash
python --version
python -m django --version
```

### Step 2 – Configure Database

If connecting to the database, configure the database in `settings.py` by providing your DB connection credentials. For example, for connecting to a PostgreSQL database:

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'YOUR_DB_NAME',
        'USER': 'postgres',
        'PASSWORD': 'YOUR_DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 3 – Migrate Models

To migrate models to PostgreSQL, install the `psycopg2` module:

```bash
pip install psycopg2
```

Run migrations:

```bash
python manage.py migrate
python manage.py migrate --run-syncdb
```

### Step 4 – Run the Application

Launch the project:

```bash
python manage.py runserver
```

### Step 5 – Register as Admin or Student

- Admins can set quizzes.
- Students can take quizzes and view results.

### Step 6 – Admin Actions

- Create quizzes with questions.
- View, modify, or delete quizzes.

### Step 7 – Student Actions

- Take quizzes.
- View quiz results.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. 
