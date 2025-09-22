# Stats Your Life API

FastAPI API to manage users and tasks with an admin panel via SQLAdmin.

## Requirements

- Python 3.12+
- PostgreSQL (or any SQL database compatible with SQLAlchemy)
- pip or Poetry for dependency management

## Installation

1. **Clone the project:**

```bash
git clone https://github.com/ton-utilisateur/stats-your-life-fastapi.git
cd stats-your-life-fastapi/stats-your-life-api
```

2. **Create a virtual environment :**
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies :**
```bash
pip install -r requirements.txt
```


##  Configuration

Edit the .env file (or app/core/config.py) with your database configuration:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
SECRET_KEY=secret_key
```

### Database and Migrations
1. **Create an Alembic migration :**
```bash
alembic revision --autogenerate -m "Initial migration"
```

2. **Apply migrations :**
```bash
alembic upgrade head
```

### Certificate and sub domain
1. **Generate certificate :**

In a "certs" folder at the project root.
```bash
mkcert api.local.stats
```
2. **Add hosts :**

Linux: /etc/hosts

Windows: C:\Windows\System32\drivers\etc\hosts
```bash
 127.0.0.1 api.local.stats
```
## Run the Application
```bash
python main.py
```

The API will be available at: http://127.0.0.1:8000/docs
<br>The admin panel will be available at: http://127.0.0.1:8000/admin