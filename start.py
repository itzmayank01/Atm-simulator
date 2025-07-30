#!/usr/bin/env python3
"""
ATM Simulator Startup Script
This script helps you quickly set up and run the ATM simulator.
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_python_version():
    """Check if Python version is 3.7 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies.")
        print("   Please run: pip install -r requirements.txt")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found.")
        return False

def setup_environment():
    """Set up environment variables if .env doesn't exist."""
    if not os.path.exists('.env'):
        print("\n🔧 Creating environment configuration...")
        env_content = """SECRET_KEY=atm-simulator-secret-key-change-in-production
DATABASE_URL=sqlite:///atm.db
FLASK_ENV=development"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Environment configuration created!")

def start_application():
    """Start the Flask application."""
    print("\n🚀 Starting ATM Simulator...")
    print("   Server will start at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    
    # Wait a moment then open browser
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the Flask app
    try:
        import app
        app.app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 ATM Simulator stopped. Thank you!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("   Try running: python app.py")

def main():
    """Main startup function."""
    print("=" * 50)
    print("🏦 ATM Simulator - SecureBank")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Setup environment
    setup_environment()
    
    # Show demo accounts
    print("\n" + "=" * 50)
    print("🔑 Demo Accounts:")
    print("   Account: 1234567890, PIN: 1234 (John Doe)")
    print("   Account: 9876543210, PIN: 5678 (Jane Smith)")
    print("   Account: 5555666677, PIN: 9999 (Bob Johnson)")
    print("=" * 50)
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()