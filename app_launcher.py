"""
Professional NLP Document Processor - Application Launcher
Enterprise-grade launcher with dependency checking and setup
Version: 1.0.0
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import importlib
from pathlib import Path

class DependencyChecker:
    """Professional dependency checker and installer."""
    
    REQUIRED_PACKAGES = {
        'tkinter': 'tkinter (usually built-in with Python)',
        'nltk': 'nltk>=3.8',
        'sentence_transformers': 'sentence-transformers>=2.2.0',
        'chromadb': 'chromadb>=0.4.0',
        'langchain': 'langchain>=0.1.0',
        'pdfplumber': 'pdfplumber>=0.9.0',
        'pytesseract': 'pytesseract>=0.3.10',
        'pdf2image': 'pdf2image>=3.1.0',
        'Pillow': 'Pillow>=9.0.0',
        'unidecode': 'unidecode>=1.3.0',
        'numpy': 'numpy>=1.21.0'
    }
    
    @classmethod
    def check_dependencies(cls):
        """Check if all required dependencies are installed."""
        missing_packages = []
        
        for package, pip_name in cls.REQUIRED_PACKAGES.items():
            try:
                if package == 'tkinter':
                    import tkinter
                elif package == 'sentence_transformers':
                    import sentence_transformers
                elif package == 'chromadb':
                    import chromadb
                elif package == 'langchain':
                    import langchain
                elif package == 'pdfplumber':
                    import pdfplumber
                elif package == 'pytesseract':
                    import pytesseract
                elif package == 'pdf2image':
                    import pdf2image
                elif package == 'Pillow':
                    import PIL
                elif package == 'unidecode':
                    import unidecode
                elif package == 'numpy':
                    import numpy
                else:
                    importlib.import_module(package)
            except ImportError:
                missing_packages.append((package, pip_name))
        
        return missing_packages
    
    @classmethod
    def install_missing_packages(cls, missing_packages):
        """Install missing packages using pip."""
        if not missing_packages:
            return True
        
        try:
            for package, pip_name in missing_packages:
                print(f"Installing {pip_name}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", pip_name
                ])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install packages: {e}")
            return False

class SystemChecker:
    """System requirements checker."""
    
    @staticmethod
    def check_python_version():
        """Check if Python version is compatible."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            return False, f"Python 3.8+ required, found {version.major}.{version.minor}"
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    
    @staticmethod
    def check_tesseract():
        """Check if Tesseract OCR is available."""
        try:
            import pytesseract
            # Try to get Tesseract version
            version = pytesseract.get_tesseract_version()
            return True, f"Tesseract {version} found"
        except:
            return False, "Tesseract OCR not found. Please install Tesseract OCR."

class LauncherGUI:
    """Professional launcher GUI."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Setup launcher window."""
        self.root.title("NLP Document Processor - Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """Setup launcher UI."""
        # Header
        header_frame = tk.Frame(self.root, bg="#0078d4", height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🤖 NLP Document Processor",
            font=("Segoe UI", 16, 'bold'),
            bg="#0078d4",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Status display
        self.status_text = tk.Text(
            main_frame,
            height=20,
            width=70,
            font=("Consolas", 10),
            bg="#3c3c3c",
            fg="white",
            insertbackground="white",
            wrap='word',
            state='disabled'
        )
        self.status_text.pack(fill='both', expand=True, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#2b2b2b")
        button_frame.pack(fill='x')
        
        self.check_btn = tk.Button(
            button_frame,
            text="Check System Requirements",
            command=self.check_system,
            font=("Segoe UI", 10),
            bg="#0078d4",
            fg="white",
            relief='flat',
            padx=20,
            pady=8
        )
        self.check_btn.pack(side='left', padx=(0, 10))
        
        self.install_btn = tk.Button(
            button_frame,
            text="Install Dependencies",
            command=self.install_dependencies,
            font=("Segoe UI", 10),
            bg="#107c10",
            fg="white",
            relief='flat',
            padx=20,
            pady=8,
            state='disabled'
        )
        self.install_btn.pack(side='left', padx=(0, 10))
        
        self.launch_btn = tk.Button(
            button_frame,
            text="Launch Application",
            command=self.launch_application,
            font=("Segoe UI", 10, 'bold'),
            bg="#ff8c00",
            fg="white",
            relief='flat',
            padx=20,
            pady=8,
            state='disabled'
        )
        self.launch_btn.pack(side='right')
        
        # Initial status
        self.log_message("Welcome to NLP Document Processor Launcher v1.0")
        self.log_message("Click 'Check System Requirements' to begin setup.")
    
    def log_message(self, message):
        """Log message to status display."""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        self.root.update()
    
    def check_system(self):
        """Check system requirements."""
        self.log_message("\n" + "="*50)
        self.log_message("CHECKING SYSTEM REQUIREMENTS")
        self.log_message("="*50)
        
        # Check Python version
        python_ok, python_msg = SystemChecker.check_python_version()
        if python_ok:
            self.log_message(f"✅ Python Version: {python_msg}")
        else:
            self.log_message(f"❌ Python Version: {python_msg}")
            messagebox.showerror("Python Version Error", python_msg)
            return
        
        # Check Tesseract
        tesseract_ok, tesseract_msg = SystemChecker.check_tesseract()
        if tesseract_ok:
            self.log_message(f"✅ Tesseract OCR: {tesseract_msg}")
        else:
            self.log_message(f"⚠️  Tesseract OCR: {tesseract_msg}")
            self.log_message("   Note: OCR functionality will be limited without Tesseract")
        
        # Check dependencies
        self.log_message("\nChecking Python packages...")
        missing_packages = DependencyChecker.check_dependencies()
        
        if not missing_packages:
            self.log_message("✅ All required packages are installed!")
            self.launch_btn.config(state='normal')
        else:
            self.log_message(f"❌ Missing {len(missing_packages)} required packages:")
            for package, pip_name in missing_packages:
                self.log_message(f"   - {package} ({pip_name})")
            self.install_btn.config(state='normal')
        
        self.log_message("\nSystem check completed.")
    
    def install_dependencies(self):
        """Install missing dependencies."""
        self.log_message("\n" + "="*50)
        self.log_message("INSTALLING DEPENDENCIES")
        self.log_message("="*50)
        
        missing_packages = DependencyChecker.check_dependencies()
        
        if not missing_packages:
            self.log_message("All packages are already installed!")
            self.launch_btn.config(state='normal')
            return
        
        self.log_message(f"Installing {len(missing_packages)} packages...")
        self.install_btn.config(state='disabled', text="Installing...")
        
        success = DependencyChecker.install_missing_packages(missing_packages)
        
        if success:
            self.log_message("✅ All packages installed successfully!")
            self.launch_btn.config(state='normal')
            self.install_btn.config(text="Install Dependencies")
        else:
            self.log_message("❌ Package installation failed!")
            self.log_message("Please install packages manually using:")
            for package, pip_name in missing_packages:
                self.log_message(f"   pip install {pip_name}")
            self.install_btn.config(state='normal', text="Install Dependencies")
    
    def launch_application(self):
        """Launch the main application."""
        self.log_message("\n" + "="*50)
        self.log_message("LAUNCHING APPLICATION")
        self.log_message("="*50)
        
        try:
            # Check if main GUI file exists
            gui_file = Path("gui/professional_gui.py")
            if not gui_file.exists():
                self.log_message("❌ Main application file not found!")
                messagebox.showerror("File Error", "gui/professional_gui.py not found!")
                return
            
            self.log_message("✅ Starting NLP Document Processor...")
            self.root.destroy()  # Close launcher
            
            # Import and run main application
            from gui.professional_gui import NLPProcessorApp
            app = NLPProcessorApp()
            app.run()
            
        except Exception as e:
            self.log_message(f"❌ Failed to launch application: {e}")
            messagebox.showerror("Launch Error", f"Failed to launch application:\n{e}")
    
    def run(self):
        """Run the launcher."""
        self.root.mainloop()

def main():
    """Main entry point."""
    print("Starting NLP Document Processor Launcher...")
    launcher = LauncherGUI()
    launcher.run()

if __name__ == "__main__":
    main()
