"""
Professional NLP Document Processing Application
Enterprise-grade GUI for document upload, processing, and querying
Author: Senior Development Team
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
from pathlib import Path
from datetime import datetime

# Import our enhanced pipeline with robust fallback
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import enhanced feedback manager and chatbot engine
try:
    from core.feedback_manager import get_feedback_manager
    print("[SUCCESS] Successfully imported FeedbackManager")
except ImportError as e:
    print(f"[ERROR] Failed to import FeedbackManager: {e}")
    get_feedback_manager = None

try:
    from core.chatbot_engine import get_chatbot_engine
    print("[SUCCESS] Successfully imported ChatbotEngine")
except ImportError as e:
    print(f"[ERROR] Failed to import ChatbotEngine: {e}")
    get_chatbot_engine = None

NLPPipeline = None
try:
    # Use absolute import only
    from pipeline.enhanced_pipeline import NLPPipeline
    print("[SUCCESS] Successfully imported NLPPipeline")
except ImportError as e:
    print(f"[ERROR] Failed to import NLPPipeline: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    NLPPipeline = None

class ModernStyle:
    """Professional styling constants."""
    PRIMARY_BG = "#2b2b2b"
    SECONDARY_BG = "#3c3c3c"
    ACCENT_BG = "#404040"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#cccccc"
    ACCENT_BLUE = "#0078d4"
    ACCENT_GREEN = "#107c10"
    ACCENT_RED = "#d13438"
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_LARGE = 14

class NLPProcessorApp:
    """Main application class."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.pipeline = None
        self.chatbot_engine = None
        self.chat_history = []  # Store chat conversations
        self.feedback_manager = get_feedback_manager() if get_feedback_manager else None
        self.performance_stats = {'queries': 0, 'cache_hits': 0, 'avg_response_time': 0}
        self.setup_window()
        self.setup_ui()
        self.initialize_pipeline()
    
    def setup_window(self):
        """Configure main window."""
        self.root.title("Professional NLP Document Processor v1.0")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernStyle.PRIMARY_BG)
        self.root.minsize(1000, 600)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_ui(self):
        """Setup the main user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg=ModernStyle.PRIMARY_BG)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Content area with tabs
        self.create_content_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create application header."""
        header_frame = tk.Frame(parent, bg=ModernStyle.ACCENT_BLUE, height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🤖 Professional NLP Document Processor",
            font=(ModernStyle.FONT_FAMILY, 18, 'bold'),
            bg=ModernStyle.ACCENT_BLUE,
            fg=ModernStyle.TEXT_PRIMARY
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Enterprise-grade AI-powered document processing and analysis",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_BLUE,
            fg=ModernStyle.TEXT_SECONDARY
        )
        subtitle_label.pack()
    
    def create_content_area(self, parent):
        """Create main content area with tabs."""
        content_frame = tk.Frame(parent, bg=ModernStyle.PRIMARY_BG)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Upload tab
        self.upload_frame = tk.Frame(self.notebook, bg=ModernStyle.PRIMARY_BG)
        self.notebook.add(self.upload_frame, text="📁 Document Upload")
        self.setup_upload_tab()
        
        # Configuration tab
        self.config_frame = tk.Frame(self.notebook, bg=ModernStyle.PRIMARY_BG)
        self.notebook.add(self.config_frame, text="⚙️ Configuration")
        self.setup_config_tab()
        
        # Query tab
        self.query_frame = tk.Frame(self.notebook, bg=ModernStyle.PRIMARY_BG)
        self.notebook.add(self.query_frame, text="🔍 Query & Search")
        self.setup_query_tab()
    
    def setup_upload_tab(self):
        """Setup document upload interface."""
        # Main container
        main_container = tk.Frame(self.upload_frame, bg=ModernStyle.PRIMARY_BG)
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(
            main_container,
            text="Document Upload & Processing",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_LARGE, 'bold'),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        title_label.pack(anchor='w', pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_container,
            text="Upload PDF, PNG, JPG, or TXT files for AI-powered analysis",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor='w', pady=(0, 30))
        
        # File selection
        file_frame = tk.LabelFrame(
            main_container,
            text="File Selection",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        file_frame.pack(fill='x', pady=(0, 20))
        
        file_input_frame = tk.Frame(file_frame, bg=ModernStyle.PRIMARY_BG)
        file_input_frame.pack(fill='x', padx=20, pady=15)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(
            file_input_frame,
            textvariable=self.file_path_var,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            bd=5
        )
        self.file_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        browse_btn = tk.Button(
            file_input_frame,
            text="Browse Files",
            command=self.browse_file,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_BLUE,
            fg=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            padx=20,
            pady=8
        )
        browse_btn.pack(side='right', padx=(10, 0))
        
        # Document ID
        id_frame = tk.Frame(file_frame, bg=ModernStyle.PRIMARY_BG)
        id_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        id_label = tk.Label(
            id_frame,
            text="Document ID (optional):",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        id_label.pack(anchor='w')
        
        self.doc_id_var = tk.StringVar()
        self.doc_id_entry = tk.Entry(
            id_frame,
            textvariable=self.doc_id_var,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            bd=5
        )
        self.doc_id_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Process button
        self.process_btn = tk.Button(
            main_container,
            text="🚀 Process Document",
            command=self.process_document,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL, 'bold'),
            bg=ModernStyle.ACCENT_GREEN,
            fg=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            padx=30,
            pady=12
        )
        self.process_btn.pack(pady=20)
        
        # Progress
        progress_frame = tk.LabelFrame(
            main_container,
            text="Processing Progress",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        progress_frame.pack(fill='x', pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', padx=20, pady=10)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to process documents",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_SECONDARY
        )
        self.progress_label.pack(padx=20, pady=(0, 10))
        
        # Results
        results_frame = tk.LabelFrame(
            main_container,
            text="Processing Results",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        results_frame.pack(fill='both', expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=12,
            font=(ModernStyle.FONT_FAMILY, 9),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            selectbackground=ModernStyle.ACCENT_BLUE,
            wrap='word'
        )
        self.results_text.pack(fill='both', expand=True, padx=20, pady=10)
    
    def setup_config_tab(self):
        """Setup configuration interface."""
        main_container = tk.Frame(self.config_frame, bg=ModernStyle.PRIMARY_BG)
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        title_label = tk.Label(
            main_container,
            text="Pipeline Configuration",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_LARGE, 'bold'),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        title_label.pack(anchor='w', pady=(0, 30))
        
        # Chunking settings
        chunk_frame = tk.LabelFrame(
            main_container,
            text="Text Chunking Settings",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        chunk_frame.pack(fill='x', pady=(0, 20))
        
        # Chunk size
        size_frame = tk.Frame(chunk_frame, bg=ModernStyle.PRIMARY_BG)
        size_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            size_frame,
            text="Chunk Size:",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(side='left')
        
        self.chunk_size_var = tk.IntVar(value=500)
        self.chunk_size_scale = tk.Scale(
            size_frame,
            from_=100,
            to=2000,
            variable=self.chunk_size_var,
            orient='horizontal',
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            highlightthickness=0
        )
        self.chunk_size_scale.pack(side='right', fill='x', expand=True, padx=(20, 0))
        
        # Overlap
        overlap_frame = tk.Frame(chunk_frame, bg=ModernStyle.PRIMARY_BG)
        overlap_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(
            overlap_frame,
            text="Chunk Overlap:",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(side='left')
        
        self.chunk_overlap_var = tk.IntVar(value=50)
        self.overlap_scale = tk.Scale(
            overlap_frame,
            from_=0,
            to=200,
            variable=self.chunk_overlap_var,
            orient='horizontal',
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            highlightthickness=0
        )
        self.overlap_scale.pack(side='right', fill='x', expand=True, padx=(20, 0))
        
        # Model selection
        model_frame = tk.LabelFrame(
            main_container,
            text="Embedding Model",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        model_frame.pack(fill='x', pady=(0, 20))
        
        model_container = tk.Frame(model_frame, bg=ModernStyle.PRIMARY_BG)
        model_container.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            model_container,
            text="Select Model:",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(anchor='w')
        
        self.model_var = tk.StringVar(value='all-MiniLM-L6-v2')
        model_combo = ttk.Combobox(
            model_container,
            textvariable=self.model_var,
            values=[
                'all-MiniLM-L6-v2',
                'all-mpnet-base-v2',
                'paraphrase-multilingual-MiniLM-L12-v2'
            ],
            state='readonly',
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL)
        )
        model_combo.pack(fill='x', pady=(5, 0))
        
        # Apply button
        apply_btn = tk.Button(
            main_container,
            text="Apply Configuration",
            command=self.apply_configuration,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL, 'bold'),
            bg=ModernStyle.ACCENT_BLUE,
            fg=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            padx=30,
            pady=12
        )
        apply_btn.pack(pady=30)
    
    def setup_query_tab(self):
        """Setup query interface."""
        main_container = tk.Frame(self.query_frame, bg=ModernStyle.PRIMARY_BG)
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        title_label = tk.Label(
            main_container,
            text="🤖 Restaurant Chatbot - Ask About Menu & Services",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_LARGE, 'bold'),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Chat controls
        controls_frame = tk.Frame(main_container, bg=ModernStyle.PRIMARY_BG)
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Cache management button
        cache_btn = tk.Button(
            controls_frame,
            text="⚡ Clear Cache",
            command=self.clear_cache,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_BLUE,
            fg=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            padx=15,
            pady=5
        )
        cache_btn.pack(side='right', padx=(0, 10))
        
        clear_btn = tk.Button(
            controls_frame,
            text="🗑️ Clear Chat",
            command=self.clear_chat_history,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_RED,
            fg=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            padx=15,
            pady=5
        )
        clear_btn.pack(side='right')
        
        # Chat history display
        chat_frame = tk.LabelFrame(
            main_container,
            text="💬 Chat History",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        chat_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.SECONDARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            wrap=tk.WORD,
            height=15,
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Initialize chat with welcome message
        self.initialize_chat_welcome()
        
        # Query input
        query_frame = tk.LabelFrame(
            main_container,
            text="💬 Ask me anything about the menu or restaurant!",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        query_frame.pack(fill='x', pady=(0, 10))
        
        query_input_frame = tk.Frame(query_frame, bg=ModernStyle.PRIMARY_BG)
        query_input_frame.pack(fill='x', padx=20, pady=15)
        
        self.query_var = tk.StringVar()
        self.query_entry = tk.Entry(
            query_input_frame,
            textvariable=self.query_var,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            bd=5
        )
        self.query_entry.pack(side='left', fill='x', expand=True, ipady=8)
        self.query_entry.bind('<Return>', lambda e: self.send_chat_message())
        
        send_btn = tk.Button(
            query_input_frame,
            text="📤 Send",
            command=self.send_chat_message,
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.ACCENT_GREEN,
            fg=ModernStyle.TEXT_PRIMARY,
            relief='flat',
            padx=20,
            pady=8
        )
        send_btn.pack(side='right', padx=(10, 0))
        
        # Sample questions
        samples_frame = tk.Frame(main_container, bg=ModernStyle.PRIMARY_BG)
        samples_frame.pack(fill='x', pady=(0, 10))
        
        samples_label = tk.Label(
            samples_frame,
            text="💡 Try asking:",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_SECONDARY
        )
        samples_label.pack(anchor='w')
        
        sample_questions = [
            "What vegetarian options do you have?",
            "What are your appetizers?",
            "Do you have gluten-free dishes?",
            "What's your most popular dish?",
            "What are your hours?",
            "Do you take reservations?"
        ]
        
        for i, question in enumerate(sample_questions):
            if i % 2 == 0:  # Create new row every 2 questions
                row_frame = tk.Frame(samples_frame, bg=ModernStyle.PRIMARY_BG)
                row_frame.pack(fill='x', pady=2)
            
            btn = tk.Button(
                row_frame,
                text=question,
                command=lambda q=question: self.set_query(q),
                font=(ModernStyle.FONT_FAMILY, 8),
                bg=ModernStyle.SECONDARY_BG,
                fg=ModernStyle.TEXT_SECONDARY,
                relief='flat',
                padx=10,
                pady=3
            )
            btn.pack(side='left', padx=(0, 10))
        
        # Results
        results_frame = tk.LabelFrame(
            main_container,
            text="Search Results",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        results_frame.pack(fill='both', expand=True)
        
        self.query_results_text = scrolledtext.ScrolledText(
            results_frame,
            font=(ModernStyle.FONT_FAMILY, 9),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            selectbackground=ModernStyle.ACCENT_BLUE,
            wrap='word'
        )
        self.query_results_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Sample queries
        samples_frame = tk.Frame(main_container, bg=ModernStyle.PRIMARY_BG)
        samples_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(
            samples_frame,
            text="Sample Queries:",
            font=(ModernStyle.FONT_FAMILY, ModernStyle.FONT_SIZE_NORMAL),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 10))
        
        sample_queries = [
            "What is machine learning?",
            "AI applications",
            "Deep learning networks"
        ]
        
        for query in sample_queries:
            btn = tk.Button(
                samples_frame,
                text=query,
                command=lambda q=query: self.set_query(q),
                font=(ModernStyle.FONT_FAMILY, 8),
                bg=ModernStyle.SECONDARY_BG,
                fg=ModernStyle.TEXT_SECONDARY,
                relief='flat',
                padx=15,
                pady=5
            )
            btn.pack(side='left', padx=(0, 10))
    
    def create_status_bar(self, parent):
        """Create status bar."""
        self.status_frame = tk.Frame(parent, bg=ModernStyle.SECONDARY_BG, height=25)
        self.status_frame.pack(fill='x', side='bottom')
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            bg=ModernStyle.SECONDARY_BG,
            fg=ModernStyle.TEXT_SECONDARY,
            font=(ModernStyle.FONT_FAMILY, 8),
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10, pady=2)
    
    def initialize_pipeline(self):
        """Initialize the NLP pipeline."""
        if NLPPipeline is None:
            self.pipeline = None
            self.update_status("❌ NLP Pipeline not available - import failed", "error")
            messagebox.showerror("Import Error", 
                               "NLP Pipeline could not be imported.\n\n"
                               "Please ensure all dependencies are installed:\n"
                               "pip install -r requirements.txt")
            return
            
        try:
            self.pipeline = NLPPipeline()
            
            # Initialize optimized chatbot engine
            if get_chatbot_engine:
                self.chatbot_engine = get_chatbot_engine(self.pipeline)
                self.update_status("✅ Enhanced Chatbot Engine initialized successfully", "success")
            else:
                self.update_status("✅ Pipeline initialized (basic mode)", "success")
                
        except Exception as e:
            self.pipeline = None
            self.chatbot_engine = None
            self.update_status(f"❌ Pipeline initialization failed: {e}", "error")
            messagebox.showerror("Pipeline Error", f"Failed to initialize pipeline:\n{e}")
    
    def browse_file(self):
        """Browse for file selection."""
        filetypes = [
            ("All Supported", "*.pdf *.png *.jpg *.jpeg *.txt"),
            ("PDF files", "*.pdf"),
            ("Image files", "*.png *.jpg *.jpeg"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Document to Process",
            filetypes=filetypes
        )
        
        if filename:
            self.file_path_var.set(filename)
            if not self.doc_id_var.get():
                doc_id = Path(filename).stem.replace(" ", "_")
                self.doc_id_var.set(doc_id)
    
    def process_document(self):
        """Process selected document."""
        # Check if pipeline is available
        if self.pipeline is None:
            messagebox.showerror("Pipeline Error", 
                               "NLP Pipeline is not initialized.\n\n"
                               "Please restart the application and ensure all dependencies are installed.")
            return
            
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showwarning("No File", "Please select a document to process.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", "Selected file does not exist.")
            return
        
        doc_id = self.doc_id_var.get() or Path(file_path).stem
        
        self.process_btn.config(state='disabled')
        self.progress_var.set(0)
        self.progress_label.config(text="Processing...")
        
        thread = threading.Thread(
            target=self._process_document_thread,
            args=(file_path, doc_id),
            daemon=True
        )
        thread.start()
    
    def _process_document_thread(self, file_path, doc_id):
        """Process document in separate thread."""
        try:
            self.root.after(0, lambda: self.progress_var.set(20))
            self.root.after(0, lambda: self.progress_label.config(text="Extracting text..."))
            
            result = self.pipeline.process_document(file_path, doc_id)
            
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self._update_results(result))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self._show_error(error_msg))
        finally:
            self.root.after(0, lambda: self.process_btn.config(state='normal'))
    
    def _update_results(self, result):
        """Update results display."""
        self.results_text.delete(1.0, tk.END)
        
        if result["status"] == "success":
            stats = result["processing_stats"]
            results_text = f"""✅ PROCESSING COMPLETED

📊 Statistics:
• Document: {result['doc_id']}
• Text length: {stats['clean_text_length']:,} characters
• Chunks: {stats['total_chunks']}
• Average chunk size: {stats['avg_chunk_size']:.1f} chars

🔢 Embeddings:
• Model: {result['embeddings_reference']['embedding_model']}
• Dimensions: {result['embeddings_reference']['embedding_dimension']}
• Collection: {result['embeddings_reference']['collection_name']}

📄 Sample chunks:
"""
            for i, chunk in enumerate(result['chunks'][:2]):
                results_text += f"\nChunk {i+1}: {chunk['text'][:150]}...\n"
            
            self.results_text.insert(1.0, results_text)
            self.progress_label.config(text="Processing completed successfully!")
            self.update_status("Document processed successfully", "success")
        else:
            error_text = f"❌ PROCESSING FAILED\n\nError: {result.get('error', 'Unknown error')}"
            self.results_text.insert(1.0, error_text)
            self.progress_label.config(text="Processing failed")
            self.update_status("Processing failed", "error")
    
    def _show_error(self, error_msg):
        """Show error message."""
        self.progress_label.config(text="Error occurred")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, f"❌ ERROR\n\n{error_msg}")
        self.update_status("Error occurred", "error")
        messagebox.showerror("Processing Error", error_msg)
    
    def apply_configuration(self):
        """Apply configuration changes."""
        try:
            config = {
                'chunk_size': self.chunk_size_var.get(),
                'chunk_overlap': self.chunk_overlap_var.get(),
                'embedding_model': self.model_var.get(),
                'collection_name': 'documents'
            }
            
            self.pipeline = NLPPipeline(**config)
            self.update_status("Configuration applied successfully", "success")
            messagebox.showinfo("Success", "Configuration updated successfully!")
            
        except Exception as e:
            self.update_status("Configuration failed", "error")
            messagebox.showerror("Error", f"Configuration failed: {e}")
    
    def set_query(self, query):
        """Set query and search."""
        self.query_var.set(query)
        self.search_documents()
    
    def search_documents(self):
        """Search documents."""
        query = self.query_var.get().strip()
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a search query.")
            return
        
        try:
            results = self.pipeline.query_documents(query, n_results=5)
            self.display_query_results(results)
        except Exception as e:
            messagebox.showerror("Search Error", f"Search failed: {str(e)}")
    
    def display_query_results(self, results):
        """Display search results."""
        self.query_results_text.delete(1.0, tk.END)
        
        if results.get("total_results", 0) > 0:
            results_text = f"🔍 Query: {results['query']}\n"
            results_text += f"📊 Found {results['total_results']} results:\n\n"
            
            for i, result in enumerate(results["results"], 1):
                similarity = result["similarity_score"]
                text = result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"]
                
                results_text += f"Result {i} (similarity: {similarity:.3f}):\n"
                results_text += f"{text}\n\n"
            
            self.query_results_text.insert(1.0, results_text)
        else:
            self.query_results_text.insert(1.0, f"No results found for: '{results['query']}'")
    
    def update_status(self, message, status_type="info"):
        """Update status bar with performance metrics."""
        colors = {
            "info": ModernStyle.TEXT_SECONDARY,
            "success": ModernStyle.ACCENT_GREEN,
            "error": ModernStyle.ACCENT_RED
        }
        
        # Add performance metrics to status message
        if self.chatbot_engine and self.performance_stats['queries'] > 0:
            cache_hit_rate = (self.performance_stats['cache_hits'] / self.performance_stats['queries']) * 100
            perf_stats = self.chatbot_engine.get_performance_stats()
            
            enhanced_message = f"{message} | Queries: {self.performance_stats['queries']} | Cache: {cache_hit_rate:.1f}% | Avg: {self.performance_stats['avg_response_time']:.3f}s"
        else:
            enhanced_message = message
        
        self.status_label.config(
            text=enhanced_message,
            fg=colors.get(status_type, ModernStyle.TEXT_SECONDARY)
        )
    
    def send_chat_message(self):
        """Send a chat message and get response."""
        query = self.query_var.get().strip()
        if not query:
            messagebox.showwarning("No Query", "Please enter a message.")
            return
        
        if self.pipeline is None:
            messagebox.showerror("Pipeline Error", "NLP Pipeline is not available.")
            return
        
        # Add user message to chat
        timestamp = datetime.now().strftime("%H:%M")
        self.add_chat_message("👤 You", query, timestamp, is_user=True)
        
        # Clear input
        self.query_var.set("")
        self.query_entry.focus()
        
        # Get AI response using optimized chatbot engine
        try:
            if self.chatbot_engine:
                # Use optimized chatbot engine with caching and performance optimizations
                response_data = self.chatbot_engine.process_query(query)
                response = response_data.get('response', 'Sorry, I could not generate a response.')
                confidence = response_data.get('confidence', 0)
                cached = response_data.get('cached', False)
                response_time = response_data.get('response_time', 0)
                
                # Add performance indicators for transparency
                perf_indicator = ""
                if cached:
                    perf_indicator = " ⚡[Cached]"
                    self.performance_stats['cache_hits'] += 1
                elif confidence > 0:
                    perf_indicator = f" (Confidence: {confidence:.1%})"
                
                response_with_meta = f"{response}{perf_indicator}"
                response_id = len(self.chat_history)
                self.add_chat_message("🤖 Restaurant Bot", response_with_meta, timestamp, is_user=False, response_id=response_id)
                
                # Store enhanced data for feedback
                self.chat_history.append({
                    'query': query,
                    'response': response,
                    'timestamp': timestamp,
                    'response_data': response_data,
                    'feedback': None,
                    'response_id': response_id,
                    'similarity_score': confidence,
                    'cached': cached,
                    'response_time': response_time
                })
                
                # Update performance stats
                self.performance_stats['queries'] += 1
                current_avg = self.performance_stats['avg_response_time']
                total_queries = self.performance_stats['queries']
                self.performance_stats['avg_response_time'] = ((current_avg * (total_queries - 1)) + response_time) / total_queries
                
            else:
                # Fallback to basic pipeline if chatbot engine not available
                results = self.pipeline.vector_db.query_with_metadata(query, n_results=3)
                
                if results and results.get('total_results', 0) > 0:
                    response = self.format_chat_response(results, query)
                    response_id = len(self.chat_history)
                    self.add_chat_message("🤖 Restaurant Bot", response, timestamp, is_user=False, response_id=response_id)
                    
                    self.chat_history.append({
                        'query': query,
                        'response': response,
                        'timestamp': timestamp,
                        'results': results,
                        'feedback': None,
                        'response_id': response_id,
                        'similarity_score': results['results'][0]['similarity_score'] if results.get('results') else 0
                    })
                else:
                    response = "I'm sorry, I couldn't find information about that in our menu or restaurant details. Could you try asking about our dishes, hours, or services?"
                    self.add_chat_message("🤖 Restaurant Bot", response, timestamp, is_user=False)
                
        except Exception as e:
            error_response = f"I'm having trouble accessing our information right now. Please try again in a moment."
            self.add_chat_message("🤖 Restaurant Bot", error_response, timestamp, is_user=False)
    
    def format_chat_response(self, results, query):
        """Format search results into a conversational response."""
        if not results or not results.get('results'):
            return "I'm sorry, I couldn't find information about that in our menu or restaurant details. Could you try asking about our dishes, hours, or services?"
        
        # Get the best result
        best_result = results['results'][0]
        best_doc = best_result['text']
        relevance = best_result['similarity_score'] * 100
        
        if relevance > 0.7:  # 70% similarity
            response = f"Based on our menu and information, here's what I found:\n\n{best_doc[:400]}"
            if len(results['results']) > 1:
                response += f"\n\nI also found some related information that might help you."
        elif relevance > 0.4:  # 40% similarity
            response = f"I found some information that might be related:\n\n{best_doc[:300]}\n\nWould you like me to search for something more specific?"
        else:
            response = f"I couldn't find a direct match, but here's some general information that might help:\n\n{best_doc[:250]}"
        
        return response
    
    def add_chat_message(self, sender, message, timestamp, is_user=False, response_id=None):
        """Add a message to the chat display."""
        self.chat_display.config(state='normal')
        
        # Add sender and timestamp
        if is_user:
            self.chat_display.insert(tk.END, f"\n{sender} ({timestamp}):\n")
            self.chat_display.insert(tk.END, f"{message}\n")
        else:
            self.chat_display.insert(tk.END, f"\n{sender} ({timestamp}):\n")
            self.chat_display.insert(tk.END, f"{message}\n")
            
            # Add feedback buttons for bot responses
            if response_id is not None:
                self.add_feedback_buttons(response_id)
        
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def add_feedback_buttons(self, response_id):
        """Add interactive feedback buttons to the chat."""
        self.chat_display.config(state='normal')
        
        # Create feedback frame
        feedback_frame = tk.Frame(self.chat_display, bg=ModernStyle.SECONDARY_BG)
        
        # Add feedback buttons
        good_btn = tk.Button(
            feedback_frame,
            text="👍 Helpful",
            command=lambda: self.collect_feedback(response_id, 'good'),
            bg=ModernStyle.ACCENT_GREEN,
            fg="white",
            font=(ModernStyle.FONT_FAMILY, 9),
            relief='flat',
            padx=10,
            pady=2
        )
        good_btn.pack(side='left', padx=5)
        
        bad_btn = tk.Button(
            feedback_frame,
            text="👎 Not Helpful",
            command=lambda: self.collect_feedback(response_id, 'bad'),
            bg=ModernStyle.ACCENT_RED,
            fg="white",
            font=(ModernStyle.FONT_FAMILY, 9),
            relief='flat',
            padx=10,
            pady=2
        )
        bad_btn.pack(side='left', padx=5)
        
        # Embed the frame in the chat display
        self.chat_display.window_create(tk.END, window=feedback_frame)
        self.chat_display.insert(tk.END, f" (Response #{response_id + 1})\n")
        
        self.chat_display.config(state='disabled')
    
    def collect_feedback(self, response_id, feedback_type):
        """Collect detailed feedback from user with optional comment."""
        if response_id >= len(self.chat_history):
            messagebox.showerror("Error", "Invalid response ID for feedback.")
            return
        
        chat_entry = self.chat_history[response_id]
        
        # Create feedback dialog
        feedback_dialog = tk.Toplevel(self.root)
        feedback_dialog.title("Provide Feedback")
        feedback_dialog.geometry("500x400")
        feedback_dialog.configure(bg=ModernStyle.PRIMARY_BG)
        feedback_dialog.transient(self.root)
        feedback_dialog.grab_set()
        
        # Center the dialog
        feedback_dialog.update_idletasks()
        x = (feedback_dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (feedback_dialog.winfo_screenheight() // 2) - (400 // 2)
        feedback_dialog.geometry(f"500x400+{x}+{y}")
        
        # Header
        header_label = tk.Label(
            feedback_dialog,
            text=f"{'👍 Positive' if feedback_type == 'good' else '👎 Negative'} Feedback",
            font=(ModernStyle.FONT_FAMILY, 14, 'bold'),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.ACCENT_GREEN if feedback_type == 'good' else ModernStyle.ACCENT_RED
        )
        header_label.pack(pady=10)
        
        # Show original question and answer
        info_frame = tk.Frame(feedback_dialog, bg=ModernStyle.SECONDARY_BG)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text="Your Question:",
            font=(ModernStyle.FONT_FAMILY, 10, 'bold'),
            bg=ModernStyle.SECONDARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        question_text = tk.Text(
            info_frame,
            height=2,
            font=(ModernStyle.FONT_FAMILY, 9),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_SECONDARY,
            wrap='word',
            state='disabled'
        )
        question_text.pack(fill='x', padx=10, pady=(0, 10))
        question_text.config(state='normal')
        question_text.insert('1.0', chat_entry['query'])
        question_text.config(state='disabled')
        
        tk.Label(
            info_frame,
            text="Bot Response:",
            font=(ModernStyle.FONT_FAMILY, 10, 'bold'),
            bg=ModernStyle.SECONDARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(anchor='w', padx=10, pady=(5, 5))
        
        answer_text = tk.Text(
            info_frame,
            height=4,
            font=(ModernStyle.FONT_FAMILY, 9),
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_SECONDARY,
            wrap='word',
            state='disabled'
        )
        answer_text.pack(fill='x', padx=10, pady=(0, 10))
        answer_text.config(state='normal')
        answer_text.insert('1.0', chat_entry['response'])
        answer_text.config(state='disabled')
        
        # Comment section
        comment_label = tk.Label(
            feedback_dialog,
            text="Additional Comments (Optional):",
            font=(ModernStyle.FONT_FAMILY, 10, 'bold'),
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY
        )
        comment_label.pack(anchor='w', padx=20, pady=(10, 5))
        
        comment_text = tk.Text(
            feedback_dialog,
            height=6,
            font=(ModernStyle.FONT_FAMILY, 10),
            bg=ModernStyle.SECONDARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            wrap='word',
            insertbackground=ModernStyle.TEXT_PRIMARY
        )
        comment_text.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(feedback_dialog, bg=ModernStyle.PRIMARY_BG)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        def submit_feedback():
            comment = comment_text.get('1.0', tk.END).strip()
            
            if self.feedback_manager:
                # Prepare enhanced metadata with chatbot engine data
                metadata = {
                    'similarity_score': chat_entry.get('similarity_score', 0),
                    'response_id': response_id,
                    'timestamp': chat_entry['timestamp'],
                    'cached': chat_entry.get('cached', False),
                    'response_time': chat_entry.get('response_time', 0),
                    'confidence': chat_entry.get('similarity_score', 0)
                }
                
                # Add response_data if available from chatbot engine
                if 'response_data' in chat_entry:
                    metadata.update({
                        'response_type': chat_entry['response_data'].get('response_type', 'unknown'),
                        'source_documents_count': len(chat_entry['response_data'].get('source_documents', []))
                    })
                
                # Save feedback using the enhanced feedback manager
                success = self.feedback_manager.add_feedback(
                    question=chat_entry['query'],
                    answer=chat_entry['response'],
                    feedback_type=feedback_type,
                    user_comment=comment,
                    metadata=metadata,
                    session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                
                if success:
                    # Update chat history
                    self.chat_history[response_id]['feedback'] = {
                        'type': feedback_type,
                        'comment': comment,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.update_status(f"Feedback saved successfully", "success")
                    messagebox.showinfo("Success", "Thank you for your feedback!")
                else:
                    messagebox.showerror("Error", "Failed to save feedback. Please try again.")
            else:
                messagebox.showerror("Error", "Feedback system not available.")
            
            feedback_dialog.destroy()
        
        def cancel_feedback():
            feedback_dialog.destroy()
        
        submit_btn = tk.Button(
            button_frame,
            text="Submit Feedback",
            command=submit_feedback,
            bg=ModernStyle.ACCENT_GREEN if feedback_type == 'good' else ModernStyle.ACCENT_RED,
            fg="white",
            font=(ModernStyle.FONT_FAMILY, 10, 'bold'),
            relief='flat',
            padx=20,
            pady=8
        )
        submit_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=cancel_feedback,
            bg=ModernStyle.ACCENT_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            font=(ModernStyle.FONT_FAMILY, 10),
            relief='flat',
            padx=20,
            pady=8
        )
        cancel_btn.pack(side='right')
        
        # Focus on comment text
        comment_text.focus()
    
    def initialize_chat_welcome(self):
        """Initialize chat display with welcome message and quick questions."""
        self.chat_display.config(state='normal')
        welcome_msg = """🤖 Welcome! I'm your restaurant assistant. Upload your menu first, then ask me anything about your dishes, hours, or services!

🍽️ Try these quick questions:
• "What are your opening hours?"
• "Do you have vegetarian options?"
• "What's your most popular dish?"
• "Do you offer delivery?"
• "What are today's specials?"
• "Do you accommodate food allergies?"

"""
        self.chat_display.insert(tk.END, welcome_msg)
        self.chat_display.config(state='disabled')
    
    def clear_cache(self):
        """Clear the chatbot engine cache with comprehensive error handling."""
        try:
            if self.chatbot_engine and hasattr(self.chatbot_engine, 'clear_cache'):
                # Get cache stats before clearing
                old_stats = self.chatbot_engine.get_performance_stats() if hasattr(self.chatbot_engine, 'get_performance_stats') else {}
                
                # Clear the cache
                self.chatbot_engine.clear_cache()
                
                # Reset performance metrics
                self.performance_stats = {'queries': 0, 'cache_hits': 0, 'avg_response_time': 0}
                
                # Reset chatbot engine metrics if available
                if hasattr(self.chatbot_engine, 'reset_metrics'):
                    self.chatbot_engine.reset_metrics()
                
                # Update status with detailed info
                cache_info = f"Cache cleared successfully"
                if old_stats.get('total_queries', 0) > 0:
                    cache_info += f" (was {old_stats.get('total_queries', 0)} queries, {old_stats.get('cache_hit_rate', '0%')} hit rate)"
                
                self.update_status(cache_info, "success")
                print(f"[SUCCESS] {cache_info}")
                
                # Show confirmation dialog
                messagebox.showinfo("Cache Cleared", 
                    "Response cache has been cleared successfully!\n\n"
                    "• All cached responses removed\n"
                    "• Performance metrics reset\n"
                    "• Next queries will generate fresh responses")
                
            elif self.chatbot_engine:
                # Chatbot engine exists but doesn't have clear_cache method
                messagebox.showwarning("Cache Management", 
                    "Cache clearing not supported by current chatbot engine.")
                self.update_status("Cache clearing not supported", "warning")
                
            else:
                # No chatbot engine available
                messagebox.showwarning("Cache Management", 
                    "Chatbot engine not available. Please initialize the pipeline first.")
                self.update_status("Chatbot engine not available", "warning")
                
        except Exception as e:
            error_msg = f"Failed to clear cache: {str(e)}"
            self.update_status(error_msg, "error")
            print(f"[ERROR] {error_msg}")
            messagebox.showerror("Cache Clear Error", 
                f"An error occurred while clearing the cache:\n\n{str(e)}\n\n"
                "Please try again or restart the application.")
    
    def clear_chat_history(self):
        """Clear the chat history."""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            try:
                # Clear chat history data
                self.chat_history.clear()
                
                # Clear the chat display
                self.chat_display.config(state='normal')
                self.chat_display.delete(1.0, tk.END)
                
                # Reset welcome message
                welcome_msg = """Welcome! I'm your restaurant assistant. Upload your menu first, then ask me anything about your dishes, hours, or services!

Try these quick questions:
• "What are your opening hours?"
• "Do you have vegetarian options?"
• "What's your most popular dish?"
• "Do you offer delivery?"
• "What are today's specials?"
• "Do you accommodate food allergies?"

"""
                self.chat_display.insert(tk.END, welcome_msg)
                self.chat_display.config(state='disabled')
                
                # Force update the display
                self.chat_display.update_idletasks()
                
                # Clear query input field
                if hasattr(self, 'query_entry'):
                    self.query_entry.delete(0, tk.END)
                
                self.update_status("Chat history cleared successfully", "success")
                print("[SUCCESS] Chat history cleared successfully")
                
            except Exception as e:
                self.update_status(f"Error clearing chat: {e}", "error")
                print(f"[ERROR] Failed to clear chat: {e}")
                messagebox.showerror("Clear Chat Error", f"Failed to clear chat history:\n{e}")

    def run(self):
        """Run the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    app = NLPProcessorApp()
    app.run()

if __name__ == "__main__":
    main()
