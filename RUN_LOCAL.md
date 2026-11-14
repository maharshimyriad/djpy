# Run Daymark Locally

These steps are for Windows and the project folder opened in VS Code.

## First-Time Setup

Open a terminal in the folder that contains `manage.py`. Create the project environment and install its dependencies:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `.venv` already exists, you can skip the first command. In Git Bash, the same Python path is `./.venv/Scripts/python.exe`.

## Start the App

Run these commands from the project folder:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/>. Create an account at <http://127.0.0.1:8000/accounts/register/>. The dashboard requires you to sign in.

The `migrate` command creates or updates the local SQLite database. You do not need to create an administrator account to use the project. To use Django Admin, run `.\.venv\Scripts\python.exe manage.py createsuperuser` and follow the terminal prompts; then open <http://127.0.0.1:8000/admin/>.

## Stop the App

Click the terminal running Django and press `Ctrl+C`.

## If Something Goes Wrong

- If you see `No module named django`, install dependencies with `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- If port 8000 is busy, start Django with `.\.venv\Scripts\python.exe manage.py runserver 8001` and open <http://127.0.0.1:8001/>.
- Bootstrap, icons, and fonts load from CDNs, so those visual assets need an internet connection. Django's pages and local database run on your computer.
