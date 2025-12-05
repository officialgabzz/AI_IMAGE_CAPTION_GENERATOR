#!/usr/bin/env python3
"""
Quick start script for AI Image Caption Generator
This script helps set up and run the application
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def check_venv():
    """Check if running in virtual environment"""
    print_header("Checking Virtual Environment")
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if not in_venv:
        print("⚠️  Not running in a virtual environment!")
        print("   It's recommended to use a virtual environment.")
        response = input("   Continue anyway? (y/n): ")
        if response.lower() != "y":
            print("\n   Create a virtual environment with:")
            print("   python -m venv venv")
            print("   source venv/bin/activate  # On macOS/Linux")
            print("   venv\\Scripts\\activate     # On Windows")
            sys.exit(1)
    else:
        print("✓ Running in virtual environment")


def install_dependencies():
    """Install required dependencies"""
    print_header("Installing Dependencies")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        sys.exit(1)

    print("Installing packages... This may take a few minutes.")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"]
        )
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Try manually: pip install -r requirements.txt")
        sys.exit(1)


def download_models():
    """Download AI models"""
    print_header("Downloading AI Models")
    print("This will download ~2GB of data. This may take 5-15 minutes.")
    response = input("Download models now? (y/n): ")

    if response.lower() == "y":
        try:
            subprocess.check_call([sys.executable, "-m", "src.models.download_models"])
            print("✓ Models downloaded successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Model download failed")
            print("   You can download them later with:")
            print("   python -m src.models.download_models")
    else:
        print("⚠️  Skipping model download")
        print("   Remember to download models before running the app!")


def create_env_file():
    """Create .env file from example"""
    print_header("Creating Configuration")

    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return

    if os.path.exists(".env.example"):
        import shutil

        shutil.copy(".env.example", ".env")
        print("✓ Created .env file from .env.example")
        print("   You can customize settings in .env")
    else:
        print("⚠️  .env.example not found, skipping")


def run_app():
    """Run the Flask application"""
    print_header("Starting Application")
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    try:
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except subprocess.CalledProcessError:
        print("❌ Failed to start server")
        sys.exit(1)


def main():
    """Main setup flow"""
    print("\n🖼️  AI Image Caption Generator - Setup\n")

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Run setup steps
    check_python_version()
    check_venv()

    # Ask if user wants to install dependencies
    response = input("\nInstall dependencies? (y/n): ")
    if response.lower() == "y":
        install_dependencies()

    # Create config
    create_env_file()

    # Download models
    download_models()

    # Ask if user wants to run the app
    print_header("Setup Complete!")
    response = input("Start the application now? (y/n): ")

    if response.lower() == "y":
        run_app()
    else:
        print("\nSetup complete! To start the application later, run:")
        print("   python app.py")
        print("\nOr use this setup script again:")
        print("   python setup.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted.")
        sys.exit(0)
