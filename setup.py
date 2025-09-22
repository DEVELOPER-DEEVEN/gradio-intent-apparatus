#!/usr/bin/env python3
"""
Setup script for Intent Apparatus - installs dependencies and checks system compatibility.
"""

import subprocess
import sys
import platform
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_system_compatibility():
    """Check if the system is compatible."""
    print("🔍 Checking system compatibility...")
    
    system = platform.system()
    print(f"Operating System: {system}")
    
    if system not in ["Windows", "Darwin", "Linux"]:
        print("❌ Unsupported operating system. This tool works on Windows, macOS, and Linux.")
        return False
    
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Python {python_version.major}.{python_version.minor} is not supported. Please use Python 3.8 or higher.")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} is compatible")
    
    # Check for display (important for GUI automation)
    if system == "Linux":
        display = os.environ.get("DISPLAY")
        if not display:
            print("⚠️  Warning: No DISPLAY environment variable found. GUI automation may not work in headless environments.")
    
    return True

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def setup_additional_packages():
    """Setup additional packages that might be needed."""
    system = platform.system()
    
    if system == "Linux":
        print("📦 Checking Linux-specific dependencies...")
        # For pyautogui on Linux, we might need additional packages
        try:
            import tkinter
            print("✅ tkinter is available")
        except ImportError:
            print("⚠️  tkinter not found. You may need to install python3-tk:")
            print("   Ubuntu/Debian: sudo apt-get install python3-tk")
            print("   Fedora: sudo dnf install python3-tkinter")
    
    elif system == "Darwin":  # macOS
        print("📦 macOS detected - checking accessibility permissions...")
        print("⚠️  You may need to grant accessibility permissions to your terminal/IDE")
        print("   Go to: System Preferences > Security & Privacy > Privacy > Accessibility")
    
    elif system == "Windows":
        print("📦 Windows detected - no additional setup required")

def main():
    """Main setup function."""
    print("🎯 Intent Apparatus Setup")
    print("=" * 50)
    
    # Check system compatibility
    if not check_system_compatibility():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check the error messages above.")
        sys.exit(1)
    
    # Setup additional packages
    setup_additional_packages()
    
    print("\n✅ Setup completed successfully!")
    print("\n🚀 To start the application, run:")
    print("   python app.py")
    print("\n⚠️  IMPORTANT SAFETY NOTES:")
    print("   - This tool can control your mouse and keyboard")
    print("   - Move your mouse to any corner of the screen to activate failsafe")
    print("   - Test commands carefully before using them")
    print("   - Close other important applications before testing")

if __name__ == "__main__":
    main()