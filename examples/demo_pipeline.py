"""
Demo script showing how the enhanced NLP preprocessing pipeline works.
This script demonstrates the complete workflow from document upload to querying.
"""

import os
import sys
from pathlib import Path
from enhanced_pipeline import NLPPipeline
import json

def create_sample_text_file():
    """Create a sample text file for demonstration."""
    sample_text = """
    Artificial Intelligence and Machine Learning

    Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
    that can perform tasks that typically require human intelligence. These tasks include learning, 
    reasoning, problem-solving, perception, and language understanding.

    Machine Learning is a subset of AI that focuses on the development of algorithms and statistical 
    models that enable computers to improve their performance on a specific task through experience, 
    without being explicitly programmed for every scenario.

    Deep Learning, a subset of machine learning, uses neural networks with multiple layers to model 
    and understand complex patterns in data. It has been particularly successful in areas such as 
    image recognition, natural language processing, and speech recognition.

    Applications of AI include:
    - Autonomous vehicles that can navigate roads safely
    - Medical diagnosis systems that can detect diseases from medical images
    - Natural language processing systems for translation and conversation
    - Recommendation systems used by streaming services and e-commerce platforms
    - Robotics for manufacturing and service industries

    The future of AI holds great promise, with potential applications in climate change mitigation, 
    scientific discovery, and solving complex global challenges. However, it also raises important 
    questions about ethics, privacy, and the impact on employment that society must address.
    """
    
    file_path = "E:/Ai_warmup/sample_ai_document.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_text.strip())
    
    print(f"📝 Created sample document: {file_path}")
    return file_path

def demo_basic_pipeline():
    """Demonstrate basic pipeline usage."""
    print("\n" + "="*60)
    print("🚀 DEMO: Basic Pipeline Usage")
    print("="*60)
    
    # Create sample file
    sample_file = create_sample_text_file()
    
    # Initialize pipeline with custom settings
    pipeline = NLPPipeline(
        chunk_size=300,           # Smaller chunks for demo
        chunk_overlap=50,         # 50 character overlap
        embedding_model='all-MiniLM-L6-v2',
        collection_name="demo_docs"
    )
    
    print(f"\n📊 Pipeline Configuration:")
    stats = pipeline.get_pipeline_stats()
    print(f"  - Chunk size: {stats['chunker_config']['chunk_size']}")
    print(f"  - Chunk overlap: {stats['chunker_config']['chunk_overlap']}")
    print(f"  - Embedding model: {stats['embedder_info']['model_name']}")
    print(f"  - Embedding dimension: {stats['embedder_info']['embedding_dimension']}")
    
    # Process the document
    print(f"\n🔄 Processing document...")
    result = pipeline.process_document(sample_file, "ai_basics")
    
    if result["status"] == "success":
        print(f"\n✅ Processing completed successfully!")
        
        # Show processing statistics
        stats = result["processing_stats"]
        print(f"\n📈 Processing Statistics:")
        print(f"  - Original text: {stats['original_text_length']:,} characters")
        print(f"  - Clean text: {stats['clean_text_length']:,} characters")
        print(f"  - Total chunks: {stats['total_chunks']}")
        print(f"  - Average chunk size: {stats['avg_chunk_size']:.1f} characters")
        
        # Show first few chunks
        print(f"\n📄 Sample Chunks (first 2 of {len(result['chunks'])}):")
        for i, chunk in enumerate(result['chunks'][:2]):
            print(f"\n  Chunk {i+1}:")
            print(f"    ID: {chunk['chunk_id']}")
            print(f"    Length: {chunk['char_count']} chars, {chunk['word_count']} words")
            print(f"    Text preview: {chunk['text'][:100]}...")
            print(f"    Embedding dimension: {len(chunk['embedding'])}")
        
        # Show embeddings reference
        emb_ref = result["embeddings_reference"]
        print(f"\n🔢 Embeddings Reference:")
        print(f"  - Collection: {emb_ref['collection_name']}")
        print(f"  - Model: {emb_ref['embedding_model']}")
        print(f"  - Dimension: {emb_ref['embedding_dimension']}")
        print(f"  - Stored chunks: {len(emb_ref['chunk_ids'])}")
        
        return pipeline, result
    else:
        print(f"❌ Processing failed: {result.get('error')}")
        return None, None

def demo_querying(pipeline):
    """Demonstrate querying functionality."""
    print("\n" + "="*60)
    print("🔍 DEMO: Querying Documents")
    print("="*60)
    
    # Sample queries
    queries = [
        "What is machine learning?",
        "Applications of artificial intelligence",
        "Deep learning neural networks",
        "Future of AI and ethics"
    ]
    
    for query in queries:
        print(f"\n🔎 Query: '{query}'")
        results = pipeline.query_documents(query, n_results=2)
        
        if results.get("total_results", 0) > 0:
            print(f"   Found {results['total_results']} relevant chunks:")
            
            for i, result in enumerate(results["results"][:2]):
                similarity = result["similarity_score"]
                chunk_text = result["text"][:150] + "..." if len(result["text"]) > 150 else result["text"]
                
                print(f"\n   Result {i+1} (similarity: {similarity:.3f}):")
                print(f"     Chunk ID: {result['chunk_id']}")
                print(f"     Text: {chunk_text}")
        else:
            print("   No results found")

def demo_different_configurations():
    """Demonstrate different pipeline configurations."""
    print("\n" + "="*60)
    print("⚙️  DEMO: Different Configurations")
    print("="*60)
    
    sample_file = "E:/Ai_warmup/sample_ai_document.txt"
    
    configs = [
        {"chunk_size": 200, "chunk_overlap": 20, "name": "Small chunks"},
        {"chunk_size": 500, "chunk_overlap": 100, "name": "Large chunks with overlap"},
        {"chunk_size": 1000, "chunk_overlap": 0, "name": "Very large, no overlap"}
    ]
    
    for config in configs:
        print(f"\n🔧 Configuration: {config['name']}")
        print(f"   Chunk size: {config['chunk_size']}, Overlap: {config['chunk_overlap']}")
        
        pipeline = NLPPipeline(
            chunk_size=config['chunk_size'],
            chunk_overlap=config['chunk_overlap'],
            collection_name=f"demo_{config['chunk_size']}"
        )
        
        result = pipeline.process_document(sample_file, f"ai_doc_{config['chunk_size']}")
        
        if result["status"] == "success":
            stats = result["processing_stats"]
            print(f"   Result: {stats['total_chunks']} chunks, avg size: {stats['avg_chunk_size']:.1f} chars")

def demo_pipeline_stats(pipeline):
    """Show comprehensive pipeline statistics."""
    print("\n" + "="*60)
    print("📊 DEMO: Pipeline Statistics")
    print("="*60)
    
    # Get pipeline stats
    stats = pipeline.get_pipeline_stats()
    
    print(f"\n🔧 Chunker Configuration:")
    chunker_config = stats['chunker_config']
    print(f"  - Chunk size: {chunker_config['chunk_size']}")
    print(f"  - Chunk overlap: {chunker_config['chunk_overlap']}")
    print(f"  - Separators: {chunker_config['separators'][:3]}... ({len(chunker_config['separators'])} total)")
    
    print(f"\n🤖 Embedder Information:")
    embedder_info = stats['embedder_info']
    print(f"  - Model: {embedder_info['model_name']}")
    print(f"  - Dimensions: {embedder_info['embedding_dimension']}")
    print(f"  - Description: {embedder_info.get('description', 'N/A')}")
    print(f"  - Size category: {embedder_info.get('size', 'N/A')}")
    
    print(f"\n💾 Vector Database Statistics:")
    db_stats = stats['vector_db_stats']
    print(f"  - Collection: {db_stats['collection_name']}")
    print(f"  - Total documents: {db_stats['total_documents']}")
    print(f"  - Storage location: {db_stats['persist_dir']}")

def main():
    """Run the complete demo."""
    print("🎯 Enhanced NLP Pipeline Demo")
    print("This demo shows how the enhanced pipeline processes documents and generates embeddings.")
    
    try:
        # Demo 1: Basic pipeline usage
        pipeline, result = demo_basic_pipeline()
        
        if pipeline and result:
            # Demo 2: Querying
            demo_querying(pipeline)
            
            # Demo 3: Pipeline statistics
            demo_pipeline_stats(pipeline)
            
            # Demo 4: Different configurations
            demo_different_configurations()
            
            print("\n" + "="*60)
            print("✅ Demo completed successfully!")
            print("="*60)
            print("\n💡 Key takeaways:")
            print("  - Documents are processed into configurable chunks")
            print("  - Each chunk gets rich metadata and embeddings")
            print("  - Embeddings are stored in ChromaDB for fast querying")
            print("  - The pipeline returns complete references to stored data")
            print("  - You can query documents using natural language")
            print("  - All components are highly configurable")
            
        else:
            print("❌ Demo failed during basic pipeline setup")
            
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
