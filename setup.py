#!/usr/bin/env python
"""
Automatic setup script for Smart Traffic Monitoring System
Handles environment setup for local development
"""
import os
import sys
import subprocess

def setup():
    print("🚀 Smart Traffic Monitoring System - Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print("✓ Python version check passed")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write('# Auto-generated .env file\n')
            f.write('DATABASE_URL=sqlite:///traffic_monitoring.db\n')
            f.write('SESSION_SECRET=dev_secret_key_change_in_production\n')
        print("✓ .env file created (SQLite for local development)")
    else:
        print("✓ .env file exists")
    
    # Check if venv exists
    venv_path = 'venv'
    if not os.path.exists(venv_path):
        print("📦 Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment exists")
    
    # Activate venv and install requirements
    print("📚 Installing dependencies...")
    pip_path = os.path.join(venv_path, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'pip')
    
    if os.path.exists('requirements.txt'):
        subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed")
    
    print("=" * 50)
    print("✅ Setup complete!")
    print("\nTo activate virtual environment:")
    if os.name == 'nt':
        print(f"   {venv_path}\\Scripts\\activate")
    else:
        print(f"   source {venv_path}/bin/activate")
    print("\nTo run the app:")
    print("   python main.py")
    print("\nThen open http://localhost:5000 in your browser")

if __name__ == '__main__':
    setup()
