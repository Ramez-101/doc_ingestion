#!/usr/bin/env python3
"""
Professional NLP Document Processor - Main Application Entry Point
Enterprise-grade AI-powered document processing and analysis
Version: 1.0.0

This is the main entry point for the application. It provides multiple ways to run:
1. GUI Application (default)
2. Command-line interface
3. System check and setup

Usage:
    python main.py                    # Launch GUI application
    python main.py --cli <file>       # Command-line processing
    python main.py --check           # System requirements check
    python main.py --help            # Show help
"""

import sys
import os
import argparse
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

def launch_gui():
    """Launch the professional GUI application."""
    try:
        from gui.professional_gui import NLPProcessorApp
        print("🚀 Launching Professional NLP Document Processor GUI...")
        app = NLPProcessorApp()
        app.run()
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("Please ensure all dependencies are installed.")
        print("Run: python main.py --check")
        return False
    except Exception as e:
        print(f"❌ Failed to launch GUI application: {e}")
        return False
    return True

def launch_cli(file_path: str, doc_id: str = None):
    """Launch command-line interface for document processing."""
    try:
        from pipeline.enhanced_pipeline import NLPPipeline
        
        print(f"🔄 Processing document: {file_path}")
        
        # Initialize pipeline
        pipeline = NLPPipeline()
        
        # Process document
        result = pipeline.process_document(file_path, doc_id)
        
        if result["status"] == "success":
            print("✅ Processing completed successfully!")
            stats = result["processing_stats"]
            print(f"📊 Statistics:")
            print(f"   - Document ID: {result['doc_id']}")
            print(f"   - Text length: {stats['clean_text_length']:,} characters")
            print(f"   - Total chunks: {stats['total_chunks']}")
            print(f"   - Average chunk size: {stats['avg_chunk_size']:.1f} characters")
            print(f"   - Embedding model: {result['embeddings_reference']['embedding_model']}")
            print(f"   - Collection: {result['embeddings_reference']['collection_name']}")
        else:
            print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import pipeline components: {e}")
        print("Please ensure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False
    return True

def check_system():
    """Check system requirements and dependencies."""
    try:
        # Import the launcher for system checking
        print("🔍 Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        else:
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check core dependencies
        dependencies = [
            ('tkinter', 'GUI framework'),
            ('sentence_transformers', 'AI embeddings'),
            ('chromadb', 'Vector database'),
            ('langchain', 'Text processing'),
            ('pdfplumber', 'PDF processing'),
            ('pytesseract', 'OCR engine'),
            ('PIL', 'Image processing'),
            ('numpy', 'Numerical computing')
        ]
        
        missing = []
        for dep, desc in dependencies:
            try:
                if dep == 'PIL':
                    import PIL
                else:
                    __import__(dep)
                print(f"✅ {dep} - {desc}")
            except ImportError:
                print(f"❌ {dep} - {desc} (MISSING)")
                missing.append(dep)
        
        if missing:
            print(f"\n⚠️  Missing {len(missing)} dependencies:")
            for dep in missing:
                print(f"   - {dep}")
            print("\nTo install missing dependencies:")
            print("   pip install -r requirements.txt")
            return False
        else:
            print("\n✅ All dependencies are installed!")
            return True
            
    except Exception as e:
        print(f"❌ System check failed: {e}")
        return False

def show_help():
    """Show help information."""
    help_text = """
🤖 Professional NLP Document Processor v1.0.0

DESCRIPTION:
    Enterprise-grade AI-powered document processing and analysis application.
    Supports PDF, PNG, JPG, and TXT files with advanced NLP capabilities.

USAGE:
    python main.py [OPTIONS] [FILE]

OPTIONS:
    --gui               Launch GUI application (default)
    --cli FILE          Process file via command-line interface
    --doc-id ID         Set document ID for CLI processing
    --check             Check system requirements and dependencies
    --help, -h          Show this help message

EXAMPLES:
    python main.py                           # Launch GUI
    python main.py --cli document.pdf       # Process PDF via CLI
    python main.py --cli doc.txt --doc-id my_doc  # Process with custom ID
    python main.py --check                  # Check system requirements

FEATURES:
    ✅ Multi-format support (PDF, PNG, JPG, TXT)
    ✅ Intelligent OCR for images and scanned documents
    ✅ Advanced text chunking and embedding generation
    ✅ Vector database storage with semantic search
    ✅ Professional GUI with real-time progress tracking
    ✅ Natural language querying capabilities

REQUIREMENTS:
    - Python 3.8+
    - See requirements.txt for full dependency list
    - Tesseract OCR (optional, for image processing)

For more information, see docs/README.md
"""
    print(help_text)

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Professional NLP Document Processor",
        add_help=False  # We'll handle help ourselves
    )
    
    parser.add_argument('--gui', action='store_true', 
                       help='Launch GUI application (default)')
    parser.add_argument('--cli', type=str, metavar='FILE',
                       help='Process file via command-line interface')
    parser.add_argument('--doc-id', type=str, metavar='ID',
                       help='Set document ID for CLI processing')
    parser.add_argument('--check', action='store_true',
                       help='Check system requirements and dependencies')
    parser.add_argument('--help', '-h', action='store_true',
                       help='Show help message')
    
    args = parser.parse_args()
    
    # Show help
    if args.help:
        show_help()
        return
    
    # Check system requirements
    if args.check:
        success = check_system()
        sys.exit(0 if success else 1)
    
    # Command-line interface
    if args.cli:
        if not os.path.exists(args.cli):
            print(f"❌ File not found: {args.cli}")
            sys.exit(1)
        
        success = launch_cli(args.cli, args.doc_id)
        sys.exit(0 if success else 1)
    
    # Default: Launch GUI
    success = launch_gui()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
