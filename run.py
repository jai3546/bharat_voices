#!/usr/bin/env python3
"""
Launcher script for Bharat Voices application (Windows-friendly)
"""

import os
import sys
import subprocess
from pathlib import Path
import webbrowser

# ----------------- Utility Functions ----------------- #

def check_python_version():
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required (current: {sys.version})")
        return False
    return True

def check_streamlit():
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_requirements():
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements. Run manually: pip install -r requirements.txt")
        return False

def setup_environment():
    env_file = Path(".env")
    if not env_file.exists():
        print("⚙️ Creating .env file...")
        env_content = """# Bharat Voices Configuration
DEBUG=False
WHISPER_MODEL=base
COLLECTION_TARGET=1000
DAILY_TARGET=10
"""
        env_file.write_text(env_content)
        print("✅ .env file created")

def check_dependencies():
    missing = []
    for pkg in ["streamlit", "pandas", "plotly"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    return missing

# ----------------- Main Launcher ----------------- #

def run_application():
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Use localhost instead of 0.0.0.0 to avoid ERR_ADDRESS_INVALID
    streamlit_command = [
        sys.executable, "-m", "streamlit", "run", "main.py",
        "--server.address", "127.0.0.1",
        "--server.port", "8501",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]

    print("🚀 Starting Bharat Voices...")
    print("🌐 Opening in browser: http://127.0.0.1:8501")
    
    # Open browser automatically
    webbrowser.open("http://127.0.0.1:8501")

    try:
        subprocess.run(streamlit_command)
    except KeyboardInterrupt:
        print("\n👋 Bharat Voices stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("Usage: python run.py [--setup] [--check] [--install]")
        return

    print("="*60)
    print("🗣️  BHARAT VOICES - Cultural Storytelling Platform")
    print("="*60)

    if not check_python_version():
        return

    setup_environment()

    if "--setup" in args:
        print("✅ Setup complete")
        return

    missing = check_dependencies()
    if "--check" in args:
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
        else:
            print("✅ All dependencies installed")
        return

    if missing or "--install" in args:
        if not install_requirements():
            return

    if not check_streamlit():
        print("❌ Streamlit not found. Install manually: pip install streamlit")
        return

    print("✅ All checks passed")
    run_application()

if __name__ == "__main__":
    main()
