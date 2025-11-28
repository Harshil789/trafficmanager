# Smart Traffic Monitoring System - Local Setup Guide

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ (installed and running)
- pip (Python package manager)

---

## Step 1: Install PostgreSQL

### On Windows:
1. Download from https://www.postgresql.org/download/windows/
2. Run installer
3. Remember the password you set for `postgres` user
4. Default port is 5432

### On Mac:
```bash
brew install postgresql
brew services start postgresql
```

### On Linux (Ubuntu/Debian):
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

## Step 2: Create Database

Open PostgreSQL command line:

```bash
# Windows/Mac/Linux - connect to PostgreSQL
psql -U postgres

# Inside psql, create database:
CREATE DATABASE traffic_db;

# Create a user (optional, for security):
CREATE USER traffic_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE traffic_db TO traffic_user;

# Exit psql
\q
```

---

## Step 3: Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd smart-traffic-monitoring

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your PostgreSQL credentials:

```
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/traffic_db
PGUSER=postgres
PGPASSWORD=your_postgres_password
PGHOST=localhost
PGPORT=5432
PGDATABASE=traffic_db
SESSION_SECRET=your_secret_key_here
```

**Example (if using default postgres):**
```
DATABASE_URL=postgresql://postgres:password123@localhost:5432/traffic_db
```

---

## Step 5: Run the Application

```bash
# Make sure PostgreSQL is running first!

# Development mode (auto-reloads on code changes):
python main.py

# Or production mode with gunicorn:
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

---

## Step 6: Access Dashboard

Open your browser and go to:
```
http://localhost:5000
```

You should see the Smart Traffic Monitoring dashboard with the purple gradient background.

---

## Troubleshooting

### Error: "could not translate host name "localhost" to address"
- PostgreSQL is not running
- Start it: `brew services start postgresql` (Mac) or similar for your OS

### Error: "FATAL: role "postgres" does not exist"
- You might have a different PostgreSQL installation
- List users: `psql --list`
- Use an existing user instead

### Error: "FATAL: password authentication failed"
- Wrong password in `.env`
- Check your PostgreSQL password and update DATABASE_URL

### Error: "Module not found"
- Make sure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

### Charts not loading
- Clear browser cache (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac)
- Check browser console for errors (F12)

---

## Useful PostgreSQL Commands

```bash
# Connect to database
psql -U postgres -d traffic_db

# List all databases
\l

# Connect to traffic_db
\c traffic_db

# List all tables
\dt

# View traffic_logs table
SELECT * FROM traffic_logs;

# View fog_stats table
SELECT * FROM fog_stats;

# Delete all data
DELETE FROM traffic_logs;
DELETE FROM fog_stats;

# Exit
\q
```

---

## Next Steps

1. Click "Send Single Traffic Data" to test Edge → Fog → Cloud flow
2. Click "Send Multiple Concurrent Devices" to test concurrent processing
3. Watch real-time analytics charts update
4. Click "Clear Logs" to reset everything

Enjoy exploring Fog + Edge Computing! 🚀
