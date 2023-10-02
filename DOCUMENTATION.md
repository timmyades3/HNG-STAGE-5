# HNG-STAGE-5
## View live

[View live](https://hng-task-1-2xlb.onrender.com/api/)

## Local Development Setup

Follow these steps to set up and run the Django app locally after cloning it from GitHub:

### 1. Clone the Repository

Clone the GitHub repository to your local machine using the following command:

```bash
git clone https://github.com/timmyades3/HNG_TASK_1
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
