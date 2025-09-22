#!/usr/bin/env python3
"""
Launch script for the Intent Apparatus.
Provides multiple ways to run the application.
"""

import sys
import os
import subprocess


def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import gradio
        return True, "Full Gradio interface"
    except ImportError:
        return False, "Basic web interface (install gradio for full features)"


def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("🎯 INTENT APPARATUS - Natural Language OS Automation")
    print("=" * 60)
    print()


def print_menu():
    """Print the main menu."""
    has_gradio, interface_info = check_dependencies()
    
    print("Choose how to run the Intent Apparatus:")
    print()
    print("1. 🌐 Web Interface (Built-in)")
    print("   - Runs on http://localhost:8080")
    print("   - No additional dependencies required")
    print("   - Perfect for testing and demonstration")
    print()
    
    if has_gradio:
        print("2. 🚀 Gradio Interface (Full-featured)")
        print("   - Advanced features and better UI")
        print("   - Runs on http://localhost:7860")
        print("   - Requires gradio package")
        print()
    else:
        print("2. 🚀 Gradio Interface (Not available)")
        print("   - Install gradio to enable this option")
        print("   - pip install gradio")
        print()
    
    print("3. 💻 Command Line Demo")
    print("   - Interactive text-based interface")
    print("   - Great for testing command parsing")
    print("   - No web browser required")
    print()
    
    print("4. 🧪 Run Automated Tests")
    print("   - Test all functionality automatically")
    print("   - Useful for verification")
    print()
    
    print("5. ⚙️  Install Dependencies")
    print("   - Run the setup script")
    print("   - Install required packages")
    print()


def launch_web_interface():
    """Launch the basic web interface."""
    print("🌐 Starting built-in web interface...")
    print("⚠️  Running in DEMO mode with simulated actions")
    print("📝 Install pyautogui for real OS automation")
    print()
    
    try:
        import web_server
        web_server.start_server(8080)
    except ImportError as e:
        print(f"❌ Error importing web server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped.")
        return True


def launch_gradio_interface():
    """Launch the Gradio interface."""
    print("🚀 Starting Gradio interface...")
    print("⚠️  Running in DEMO mode with simulated actions")
    print("📝 Install pyautogui for real OS automation")
    print()
    
    try:
        import app
        app.main()
    except ImportError as e:
        print(f"❌ Error importing Gradio app: {e}")
        print("💡 Try: pip install gradio")
        return False
    except KeyboardInterrupt:
        print("\n👋 Gradio interface stopped.")
        return True


def launch_cli_demo():
    """Launch the command line demo."""
    print("💻 Starting command line demo...")
    print()
    
    try:
        import demo
        demo.demo_interface()
    except ImportError as e:
        print(f"❌ Error importing demo: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Demo stopped.")
        return True


def run_tests():
    """Run automated tests."""
    print("🧪 Running automated tests...")
    print()
    
    try:
        import demo
        demo.test_functionality()
        print("\n✅ Tests completed successfully!")
    except ImportError as e:
        print(f"❌ Error importing demo: {e}")
        return False


def install_dependencies():
    """Install dependencies."""
    print("⚙️  Installing dependencies...")
    print()
    
    if os.path.exists("setup.py"):
        try:
            subprocess.run([sys.executable, "setup.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Setup script failed. Try manual installation:")
            print("   pip install -r requirements.txt")
    else:
        print("❌ setup.py not found. Try manual installation:")
        print("   pip install -r requirements.txt")


def main():
    """Main launcher function."""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5, or 'q' to quit): ").strip().lower()
            
            if choice in ['q', 'quit', 'exit']:
                print("👋 Goodbye!")
                break
            
            elif choice == '1':
                launch_web_interface()
            
            elif choice == '2':
                has_gradio, _ = check_dependencies()
                if has_gradio:
                    launch_gradio_interface()
                else:
                    print("❌ Gradio not available. Install it first (option 5) or use option 1.")
            
            elif choice == '3':
                launch_cli_demo()
            
            elif choice == '4':
                run_tests()
            
            elif choice == '5':
                install_dependencies()
            
            else:
                print("❌ Invalid choice. Please enter 1-5 or 'q' to quit.")
            
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()