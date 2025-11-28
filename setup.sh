#!/bin/bash
# Setup script for Mac/Linux

echo "🚀 Smart Traffic Monitoring System - Setup"
echo "=================================================="

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
source venv/bin/activate

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Auto-generated .env file
DATABASE_URL=sqlite:///traffic_monitoring.db
SESSION_SECRET=dev_secret_key_change_in_production
EOF
    echo "✓ .env file created (SQLite for local development)"
else
    echo "✓ .env file exists"
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

echo "=================================================="
echo "✅ Setup complete!"
echo ""
echo "Virtual environment is activated. To run the app:"
echo "   python main.py"
echo ""
echo "Then open http://localhost:5000 in your browser"
