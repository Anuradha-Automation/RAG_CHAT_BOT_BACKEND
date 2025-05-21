```markdown
# RAG Backend Django Setup

This document provides a comprehensive guide to setting up the RAG Backend Django project.

## Python Installation

Ensure Python is installed on your system. If not, download and install it from [python.org](https://www.python.org/downloads/).  Python 3.7 or higher is recommended.

## Project Setup

1. **Clone the Repository:**

```bash
git clone [https://github.com/exoticaitsolutions/RAG_Backend.git](https://github.com/exoticaitsolutions/RAG_Backend.git)
cd RAG_Backend
```

2. **Setup Options:**

Choose between the automatic setup script (recommended) or the manual setup.

### Option 1: Automatic Setup (Recommended)

This method simplifies the process.

* **Windows:**

```bash
setup.bat
```

* **Unix/macOS/Linux:**

```bash
bash setup.sh
```

The automatic script handles virtual environment creation, activation, dependency installation, and database configuration.  If you encounter issues, proceed with the manual setup.

### Option 2: Manual Setup

This method offers more control.

1. **Create and Activate a Virtual Environment:**

* **Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

* **Unix/macOS/Linux:**

```bash
python3 -m venv .venv  # Use python3 if your default python is Python 2
source .venv/bin/activate
```

2. **Upgrade pip (Recommended):**

```bash
pip install --upgrade pip
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables (.env):**

Create a `.env` file in the project's root directory.  **Do not commit this file to version control.**  Populate it with your settings:

BASE_API_URL=[invalid URL removed]  # Or your deployed URL


# Database settings (Example: MySQL)
DB_TYPE=mysql  # or postgresql, etc.
DB_NAME="database_name"
DB_USER="database_user_name"
DB_PASSWORD="database_password"
DB_HOST="database_hostname"  # e.g., localhost, 127.0.0.1, or a remote host
DB_PORT=3306  # Adjust if necessary

# OpenAI API Key
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"  # Replace with your actual key
```
**Important:** Replace placeholders like `"database_name"`, `"database_user_name"`, `"database_password"`, `"database_hostname"`, and `YOUR_OPENAI_API_KEY` with your actual credentials.

5. **Database Migrations:**

```bash
python manage.py makemigrations RAG_CHATBOT_BACKEND_APIS
python manage.py migrate
```

6. **Seed Data (Optional):**

```bash
python manage.py seed_data  # Seeds initial data (e.g., countries, states).
```

7. **Run the Development Server:**

```bash
python manage.py runserver
```

Or, to run on a specific port:

```bash
python manage.py runserver 9000  # Example: runs on port 8080
```

After successfully completing the setup (automatic or manual), you can start the development server using the command:

```bash
python manage.py runserver
```

This will start the server at `http://127.0.0.1:8000/` (or the port you specified). You can then access your Django application in your web browser.  If you are running the server on a remote machine, you might need to configure your firewall and adjust the `BASE_API_URL` accordingly.

## Troubleshooting

* **Dependency Issues:** Ensure the correct Python version and activated virtual environment.  Try upgrading `pip` before installing requirements.  Check for conflicting package versions.
* **Database Connection Errors:** Verify database credentials in `.env`. Ensure the database server is running and accessible. Check firewall rules if connecting remotely.
* **Missing .env File:** Create the `.env` file and populate it.
* **Port Conflicts:** Use a different port if 8000 is in use.
* **`python` vs. `python3`:** Use `python3` if your default `python` points to Python 2.
* **Migrations Issues:** If you have issues with migrations, you might need to delete migration files in your app's `migrations` directory (except `__init__.py`) and try again.  Ensure your database is in a consistent state.
* **OpenAI API Key Issues:** Ensure your API key is valid and has the necessary permissions.  Check OpenAI's documentation for rate limits.


##  Important Considerations

* **Security:**  Never commit your `.env` file containing sensitive information to version control.
* **Database:**  This guide uses MySQL as an example. Adjust the settings in `.env` if you are using a different database (PostgreSQL, SQLite, etc.).  Make sure the database is created before running migrations.
* **OpenAI API Key:**  Obtain your OpenAI API key from the OpenAI website and replace the placeholder in the `.env` file.
* **Virtual Environment:**  Always use a virtual environment to isolate your project's dependencies.
* **Automatic Setup:** The automatic setup script is highly recommended for its simplicity.  Only resort to the manual method if you encounter problems with the script.


```

Key changes:

* Added the crucial `python manage.py runserver` command *after* the setup instructions.  This makes it clear when and how to start the server.
* Added a brief explanation of what the `runserver` command does and how to access the application in a browser.
* Added a note about accessing the server on a remote machine.  This is important for deployment scenarios.
* Minor wording improvements for clarity.
