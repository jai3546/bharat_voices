"""
Setup script for Bharat Voices application
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "uploads",
        "exports",
        "cache",
        "logs",
        ".streamlit"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_environment():
    """Setup environment configuration"""
    env_file = ".env"
    env_example = ".env.example"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            # Copy example to .env
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print(f"✅ Created {env_file} from {env_example}")
        else:
            # Create basic .env file
            basic_env = """# Bharat Voices Environment Configuration
DEBUG=False
GOOGLE_CREDENTIALS_PATH=credentials.json
WHISPER_MODEL=base
COLLECTION_TARGET=1000
"""
            with open(env_file, 'w') as f:
                f.write(basic_env)
            print(f"✅ Created basic {env_file}")
    else:
        print(f"✅ {env_file} already exists")

def create_google_credentials_template():
    """Create template for Google credentials"""
    credentials_file = "credentials.json.template"
    
    if not os.path.exists(credentials_file):
        template = {
            "type": "service_account",
            "project_id": "your-project-id",
            "private_key_id": "your-private-key-id",
            "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
            "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
            "client_id": "your-client-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
        }
        
        with open(credentials_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"✅ Created {credentials_file}")
        print("📝 Please update this file with your actual Google Service Account credentials")

def check_streamlit():
    """Check if Streamlit is properly installed"""
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} is installed")
        return True
    except ImportError:
        print("❌ Streamlit is not installed")
        return False

def create_sample_data():
    """Create sample data for testing"""
    sample_data_file = "data/sample_submissions.json"
    
    if not os.path.exists(sample_data_file):
        sample_data = [
            {
                "id": "sample_1",
                "title": "The Wise Tree",
                "content": "A tree that gives shade cannot complain about the sun.",
                "content_type": "Proverb",
                "language": "English",
                "category": "Wisdom & Life Lessons",
                "likes": 15,
                "featured": True
            },
            {
                "id": "sample_2", 
                "title": "Unity in Diversity",
                "content": "Many rivers flow into one ocean, yet the ocean remains one.",
                "content_type": "Saying",
                "language": "English", 
                "category": "Family & Community",
                "likes": 8,
                "featured": False
            }
        ]
        
        with open(sample_data_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"✅ Created sample data: {sample_data_file}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your API keys and configuration")
    print("2. If using Google Sheets, update credentials.json with your service account key")
    print("3. Run the application with: streamlit run main.py")
    print("4. Open your browser to http://localhost:8501")
    print("\n📚 Documentation:")
    print("- Google Sheets API: https://developers.google.com/sheets/api")
    print("- Hugging Face API: https://huggingface.co/docs/api-inference/index")
    print("- Whisper: https://github.com/openai/whisper")
    print("\n🆘 Need help? Check the README.md file or create an issue on GitHub")

def main():
    """Main setup function"""
    print("🚀 Setting up Bharat Voices...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Some packages failed to install. You may need to install them manually.")
    
    # Check Streamlit
    if not check_streamlit():
        print("❌ Please install Streamlit manually: pip install streamlit")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create credentials template
    create_google_credentials_template()
    
    # Create sample data
    create_sample_data()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
