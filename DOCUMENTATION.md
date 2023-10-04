# HNG-STAGE-5
## View live

[View live](https://hng-stage-5.onrender.com)

## Local Development Setup

Follow these steps to set up and run the Django app locally after cloning it from GitHub:

### 1. Clone the Repository

Clone the GitHub repository to your local machine using the following command:

```bash
https://github.com/timmyades3/HNG-STAGE-5
```

### 2. Create a Virtual Environment

Navigate to the project directory and create a virtual environment:

```bash
cd your-django-app
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS and Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Change the `.envexample` file in the project root to `.env`; it contains necessary environment variables. You can usually find these settings in your project's `settings.py` file.

### 6. Apply Database Migrations

Apply the database migrations to create the database schema:

```bash
python manage.py makemigrations
```

After that run:

```bash
python manage.py migrate
```

### 7. Create a Superuser (Optional)

If your app has user authentication and you want to create an admin user, run:

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

The server should be accessible at `http://localhost:8000/` in your web browser.

## Endpoints

- upload video `endpoint/`


## Usage

To use this API effectively, follow these steps:

1. Start the server.
2. Use Postman or any apk you prefer to interact with the API endpoints.

## link to my endpoint video
https://drive.google.com/file/d/1E79x1RylUhimPmiYuRjFIIOtI8CcOck7/view?usp=sharing
