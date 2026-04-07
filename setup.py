#!/usr/bin/env python3
"""
PersonaAI Setup Script
======================
Initialize and configure PersonaAI system
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Tuple
import platform


class PersonaAISetup:
    """Setup wizard for PersonaAI"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / '.env'
        self.config_file = self.project_root / 'config.ini'
        self.venv_dir = self.project_root / 'venv'
        
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60 + "\n")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"✅ {text}")
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"❌ {text}")
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"ℹ️  {text}")
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        self.print_header("Checking Python Version")
        
        version = sys.version_info
        required_version = (3, 8)
        
        if version >= required_version:
            self.print_success(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
            return True
        else:
            self.print_error(f"Python 3.8+ required. Found {version.major}.{version.minor}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check system dependencies"""
        self.print_header("Checking System Dependencies")
        
        dependencies = {
            'git': 'Git version control',
            'pip': 'Python package manager'
        }
        
        all_found = True
        
        for cmd, description in dependencies.items():
            try:
                result = subprocess.run(
                    ['which', cmd] if platform.system() != 'Windows' else ['where', cmd],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.print_success(f"{description} is installed")
                else:
                    self.print_error(f"{description} is not installed")
                    all_found = False
            except Exception as e:
                self.print_error(f"Could not check for {description}: {e}")
                all_found = False
        
        return all_found
    
    def create_virtual_environment(self) -> bool:
        """Create Python virtual environment"""
        self.print_header("Creating Virtual Environment")
        
        if self.venv_dir.exists():
            self.print_info(f"Virtual environment already exists at {self.venv_dir}")
            return True
        
        try:
            self.print_info(f"Creating virtual environment at {self.venv_dir}...")
            subprocess.run(
                [sys.executable, '-m', 'venv', str(self.venv_dir)],
                check=True,
                capture_output=True
            )
            self.print_success("Virtual environment created successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        self.print_header("Installing Dependencies")
        
        requirements_file = self.project_root / 'requirements.txt'
        
        if not requirements_file.exists():
            self.print_error(f"requirements.txt not found at {requirements_file}")
            return False
        
        try:
            self.print_info(f"Installing packages from {requirements_file}...")
            
            if platform.system() == 'Windows':
                pip_path = self.venv_dir / 'Scripts' / 'pip.exe'
            else:
                pip_path = self.venv_dir / 'bin' / 'pip'
            
            subprocess.run(
                [str(pip_path), 'install', '-r', str(requirements_file)],
                check=True,
                capture_output=True
            )
            
            self.print_success("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_environment_variables(self) -> bool:
        """Setup environment variables"""
        self.print_header("Setting Up Environment Variables")
        
        if self.env_file.exists():
            self.print_info(f".env file already exists at {self.env_file}")
            return True
        
        print("\nPlease provide your API keys:")
        print("(Leave blank to skip, you can add them later)\n")
        
        api_keys = {}
        
        # TMDb API
        tmdb_key = input("TMDb API Key (get it from https://www.themoviedb.org/settings/api): ").strip()
        if tmdb_key:
            api_keys['TMDB_API_KEY'] = tmdb_key
        
        # Spotify API
        spotify_id = input("Spotify Client ID: ").strip()
        spotify_secret = input("Spotify Client Secret: ").strip()
        if spotify_id and spotify_secret:
            api_keys['SPOTIFY_CLIENT_ID'] = spotify_id
            api_keys['SPOTIFY_CLIENT_SECRET'] = spotify_secret
        
        # News API
        news_key = input("News API Key (get it from https://newsapi.org): ").strip()
        if news_key:
            api_keys['NEWS_API_KEY'] = news_key
        
        # Write to .env file
        try:
            with open(self.env_file, 'w') as f:
                f.write("# PersonaAI Environment Variables\n")
                f.write("# Auto-generated by setup script\n\n")
                
                for key, value in api_keys.items():
                    f.write(f"{key}={value}\n")
                
                # Add defaults
                f.write("\n# Optional settings\n")
                f.write("DATABASE_URL=sqlite:///personaai.db\n")
                f.write("DEBUG=false\n")
                f.write("LOG_LEVEL=INFO\n")
            
            self.print_success(f".env file created at {self.env_file}")
            
            if api_keys:
                self.print_info(f"Configured {len(api_keys)} API key(s)")
            else:
                self.print_info("No API keys configured. Add them to .env file later.")
            
            return True
        except Exception as e:
            self.print_error(f"Failed to create .env file: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verify installation by importing key modules"""
        self.print_header("Verifying Installation")
        
        modules_to_check = [
            'streamlit',
            'pandas',
            'numpy',
            'sklearn',
            'plotly',
            'requests'
        ]
        
        all_ok = True
        
        for module in modules_to_check:
            try:
                __import__(module)
                self.print_success(f"{module} is available")
            except ImportError:
                self.print_error(f"{module} is not available")
                all_ok = False
        
        return all_ok
    
    def create_directories(self) -> bool:
        """Create necessary directories"""
        self.print_header("Creating Directories")
        
        directories = [
            self.project_root / 'data',
            self.project_root / 'exports',
            self.project_root / 'logs',
            self.project_root / '.streamlit'
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                self.print_success(f"Created directory: {directory}")
            except Exception as e:
                self.print_error(f"Failed to create directory {directory}: {e}")
                return False
        
        return True
    
    def create_streamlit_config(self) -> bool:
        """Create Streamlit configuration"""
        self.print_header("Creating Streamlit Configuration")
        
        streamlit_dir = self.project_root / '.streamlit'
        config_file = streamlit_dir / 'config.toml'
        
        if config_file.exists():
            self.print_info("Streamlit config already exists")
            return True
        
        try:
            config_content = """[theme]
primaryColor = "#00D9FF"
backgroundColor = "#0a0e27"
secondaryBackgroundColor = "#1a1f3a"
textColor = "#ffffff"
font = "sans serif"

[client]
showErrorDetails = false

[server]
maxUploadSize = 200
port = 8501

[logger]
level = "info"

[client.logger]
enableLogger = true
"""
            
            with open(config_file, 'w') as f:
                f.write(config_content)
            
            self.print_success(f"Created Streamlit config at {config_file}")
            return True
        except Exception as e:
            self.print_error(f"Failed to create Streamlit config: {e}")
            return False
    
    def print_next_steps(self):
        """Print next steps"""
        self.print_header("Next Steps")
        
        print("Setup completed! Here's what to do next:\n")
        
        print("1. Activate the virtual environment:")
        if platform.system() == 'Windows':
            print(f"   .\\venv\\Scripts\\activate")
        else:
            print(f"   source venv/bin/activate")
        
        print("\n2. Run the application:")
        print("   streamlit run recommendation_system.py")
        
        print("\n3. Open your browser to:")
        print("   http://localhost:8501")
        
        print("\n4. (Optional) Add API keys to .env file:")
        print(f"   Edit {self.env_file}")
        
        print("\n5. Read the documentation:")
        print("   cat README.md")
        
        print("\n" + "="*60 + "\n")
    
    def run(self) -> bool:
        """Run complete setup"""
        print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║               🎉 PersonaAI Setup Wizard 🎉                ║
║                                                            ║
║        Intelligent Recommendation System with ML           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
        """)
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("System Dependencies Check", self.check_dependencies),
            ("Create Virtual Environment", self.create_virtual_environment),
            ("Create Directories", self.create_directories),
            ("Install Dependencies", self.install_dependencies),
            ("Setup Environment Variables", self.setup_environment_variables),
            ("Create Streamlit Config", self.create_streamlit_config),
            ("Verify Installation", self.verify_installation),
        ]
        
        failed_steps = []
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    failed_steps.append(step_name)
            except Exception as e:
                self.print_error(f"Unexpected error in {step_name}: {e}")
                failed_steps.append(step_name)
        
        if failed_steps:
            self.print_header("⚠️  Setup Completed with Issues")
            print(f"Failed steps: {', '.join(failed_steps)}\n")
            print("Please fix these issues and try again.")
            return False
        
        self.print_header("✅ Setup Completed Successfully")
        self.print_next_steps()
        
        return True


def main():
    """Main entry point"""
    setup = PersonaAISetup()
    success = setup.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
