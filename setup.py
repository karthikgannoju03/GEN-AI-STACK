#!/usr/bin/env python3
"""
Setup script for GenAI Stack
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        return False
    print("✅ Python version is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    success, output = run_command("node --version")
    if not success:
        print("❌ Node.js is not installed")
        return False
    print(f"✅ Node.js version: {output.strip()}")
    return True

def install_dependencies():
    """Install all dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Install root dependencies
    print("Installing root dependencies...")
    success, output = run_command("npm install")
    if not success:
        print(f"❌ Failed to install root dependencies: {output}")
        return False
    
    # Install frontend dependencies
    print("Installing frontend dependencies...")
    success, output = run_command("npm install", cwd="frontend")
    if not success:
        print(f"❌ Failed to install frontend dependencies: {output}")
        return False
    
    # Install backend dependencies
    print("Installing backend dependencies...")
    success, output = run_command("pip install -r requirements.txt", cwd="backend")
    if not success:
        print(f"❌ Failed to install backend dependencies: {output}")
        return False
    
    print("✅ All dependencies installed successfully")
    return True

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("\n🔧 Setting up environment file...")
        env_example.rename(env_file)
        print("✅ Environment file created from template")
        print("⚠️  Please edit .env file with your configuration")
    elif env_file.exists():
        print("✅ Environment file already exists")
    else:
        print("❌ No environment template found")

def main():
    """Main setup function"""
    print("🚀 GenAI Stack Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        print("Please install Node.js 18+ from https://nodejs.org/")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Set up your database (PostgreSQL/Supabase)")
    print("3. Run: npm run dev")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
