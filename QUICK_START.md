# Quick Start Guide - Smart Traffic Monitoring System

## For Local Development (Easiest Setup!)

### **Windows Users:**
```bash
# 1. Open Command Prompt or PowerShell
# 2. Navigate to project folder
cd smart-traffic-monitoring

# 3. Run setup script (auto-creates everything)
setup.bat

# 4. Run the app
python main.py
```

### **Mac/Linux Users:**
```bash
# 1. Open Terminal
# 2. Navigate to project folder
cd smart-traffic-monitoring

# 3. Make setup script executable
chmod +x setup.sh

# 4. Run setup script (auto-creates everything)
./setup.sh

# 5. Run the app
python main.py
```

### **Or use Python setup (All platforms):**
```bash
python setup.py
# Follow the instructions
python main.py
```

---

## What Gets Auto-Setup:

✅ **Virtual Environment** - Created automatically  
✅ **Dependencies** - Installed from requirements.txt  
✅ **.env File** - Auto-generated with SQLite database  
✅ **Database** - SQLite (no PostgreSQL needed!)  
✅ **Session Secret** - Auto-generated  

---

## Access Your App

Once running, open your browser:
```
http://localhost:5000
```

You should see the Smart Traffic Monitoring dashboard with:
- Purple gradient background
- Three architecture cards (Edge, Fog, Cloud)
- Real-time analytics charts
- Control buttons

---

## First Time Setup Checklist

- [ ] Clone/pull the repository
- [ ] Run setup script (`setup.bat`, `setup.sh`, or `setup.py`)
- [ ] Run `python main.py`
- [ ] Open `http://localhost:5000` in browser
- [ ] Test by clicking "Send Single Traffic Data"
- [ ] Verify charts populate with data

---

## Troubleshooting

### App won't start
- Make sure Python 3.8+ is installed: `python --version`
- Check if port 5000 is free: `lsof -i :5000`

### Virtual environment not working
- Manually activate: 
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- Then: `pip install -r requirements.txt`

### ModuleNotFoundError
- Activate virtual environment first
- Run: `pip install -r requirements.txt` again

### Port 5000 already in use
- Change port in main.py or kill process using port 5000

---

## Next Steps

1. Click **"Send Single Traffic Data"** - Tests Edge→Fog→Cloud flow
2. Click **"Send Multiple Concurrent Devices"** - Tests multi-threading (3+ devices)
3. Watch **three real-time charts** update automatically
4. Click **"Clear Logs"** - Resets all data and graphs
5. Check **console logs** at bottom for system activity

---

## Push to GitHub & Pull Locally

### Workflow:
1. **On Replit:** Make changes, test them
2. **Commit & Push:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

3. **On Local Machine:**
   ```bash
   git pull origin main
   python main.py
   ```

That's it! No manual database setup needed anymore! 🎉

---

## File Structure

```
smart-traffic-monitoring/
├── app.py                  # Main Flask app (auto-config)
├── models.py              # Database models
├── fog.py                 # Fog layer logic
├── cloud.py               # Cloud layer logic
├── edge_simulator.py      # Edge device simulator
├── main.py                # Entry point
├── requirements.txt       # All dependencies
├── setup.py              # Python setup script
├── setup.sh              # Mac/Linux setup script
├── setup.bat             # Windows setup script
├── .env                  # Auto-generated (SQLite)
├── .gitignore            # Excludes venv, .env, __pycache__
├── templates/
│   └── index.html        # Dashboard UI
└── traffic_monitoring.db # SQLite database (auto-created)
```

---

**That's all you need! Just run the setup script and you're good to go!** 🚀
