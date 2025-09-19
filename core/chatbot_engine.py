"""
Enhanced Chatbot Engine for Restaurant Q&A System
Optimized end-to-end pipeline with caching and performance optimizations
Version: 1.0.0
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ResponseCache:
    """Intelligent response caching system to reduce LLM overhead."""
    
    def __init__(self, cache_dir: str = "./cache", max_age_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "response_cache.json"
        self.max_age_hours = max_age_hours
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache from disk."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cache to disk."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def _generate_key(self, query: str, doc_context: str = "") -> str:
        """Generate cache key from query and context."""
        content = f"{query.lower().strip()}|{doc_context}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, query: str, doc_context: str = "") -> Optional[Dict[str, Any]]:
        """Get cached response if available and not expired."""
        key = self._generate_key(query, doc_context)
        
        if key in self.cache:
            entry = self.cache[key]
            cached_time = datetime.fromisoformat(entry['timestamp'])
            
            if datetime.now() - cached_time < timedelta(hours=self.max_age_hours):
                logger.info(f"Cache hit for query: {query[:50]}...")
                return entry['response']
            else:
                # Remove expired entry
                del self.cache[key]
                self._save_cache()
        
        return None
    
    def set(self, query: str, response: Dict[str, Any], doc_context: str = ""):
        """Cache response for future use."""
        key = self._generate_key(query, doc_context)
        
        self.cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'doc_context': doc_context[:100]  # Store snippet for debugging
        }
        
        self._save_cache()
        logger.info(f"Cached response for query: {query[:50]}...")

class OptimizedChatbotEngine:
    """
    High-performance chatbot engine with caching and optimization.
    Designed for restaurant Q&A with menu/FAQ support.
    """
    
    def __init__(self, pipeline=None, cache_responses: bool = True):
        """Initialize the optimized chatbot engine."""
        self.pipeline = pipeline
        self.cache = ResponseCache() if cache_responses else None
        self.response_templates = self._load_response_templates()
        self.performance_metrics = {
            'total_queries': 0,
            'cache_hits': 0,
            'avg_response_time': 0,
            'last_reset': datetime.now().isoformat()
        }
        
        logger.info("Optimized Chatbot Engine initialized")
    
    def _load_response_templates(self) -> Dict[str, str]:
        """Load response templates for common scenarios."""
        return {
            'greeting': "Hello! I'm your restaurant assistant. I can help you with information about our menu, hours, services, and more. What would you like to know?",
            'no_results': "I'm sorry, I couldn't find specific information about that in our menu or restaurant details. Could you try asking about our dishes, hours, location, or services?",
            'low_confidence': "I found some information that might be related to your question. Here's what I have:",
            'high_confidence': "Based on our menu and restaurant information, here's what I found:",
            'error': "I'm having trouble accessing our information right now. Please try again in a moment, or feel free to call us directly.",
            'feedback_thanks': "Thank you for your feedback! It helps us improve our service."
        }
    
    def process_query(self, query: str, doc_id_filter: str = None) -> Dict[str, Any]:
        """
        Process user query with optimization and caching.
        
        Args:
            query: User's question
            doc_id_filter: Optional filter by document ID
            
        Returns:
            Comprehensive response with metadata
        """
        start_time = time.time()
        self.performance_metrics['total_queries'] += 1
        
        try:
            # Check cache first
            if self.cache:
                cached_response = self.cache.get(query, doc_id_filter or "")
                if cached_response:
                    self.performance_metrics['cache_hits'] += 1
                    cached_response['cached'] = True
                    cached_response['response_time'] = time.time() - start_time
                    return cached_response
            
            # Process query through pipeline
            if not self.pipeline:
                return self._create_error_response("Pipeline not available")
            
            # Get search results
            search_results = self.pipeline.query_documents(
                query, 
                n_results=5, 
                doc_id_filter=doc_id_filter
            )
            
            # Generate optimized response
            response = self._generate_optimized_response(query, search_results)
            
            # Add performance metadata
            response_time = time.time() - start_time
            response['response_time'] = response_time
            response['cached'] = False
            response['timestamp'] = datetime.now().isoformat()
            
            # Update performance metrics
            self._update_performance_metrics(response_time)
            
            # Cache the response
            if self.cache:
                self.cache.set(query, response, doc_id_filter or "")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
            return self._create_error_response(str(e))
    
    def _generate_optimized_response(self, query: str, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized response based on search results."""
        
        if not search_results or search_results.get('total_results', 0) == 0:
            return {
                'response': self.response_templates['no_results'],
                'confidence': 0.0,
                'source_documents': [],
                'response_type': 'no_results'
            }
        
        # Get best result
        best_result = search_results['results'][0]
        similarity_score = best_result['similarity_score']
        
        # Determine response strategy based on confidence
        if similarity_score > 0.8:
            response_type = 'high_confidence'
            response_text = self._format_high_confidence_response(best_result, search_results)
        elif similarity_score > 0.5:
            response_type = 'medium_confidence'
            response_text = self._format_medium_confidence_response(best_result, search_results)
        else:
            response_type = 'low_confidence'
            response_text = self._format_low_confidence_response(best_result, search_results)
        
        return {
            'response': response_text,
            'confidence': similarity_score,
            'source_documents': search_results['results'][:3],  # Top 3 sources
            'response_type': response_type,
            'query': query
        }
    
    def _format_high_confidence_response(self, best_result: Dict, search_results: Dict) -> str:
        """Format high-confidence response."""
        content = best_result['text']
        
        # Truncate if too long
        if len(content) > 400:
            content = content[:400] + "..."
        
        response = f"{self.response_templates['high_confidence']}\n\n{content}"
        
        # Add additional context if available
        if len(search_results['results']) > 1:
            response += "\n\nI also found some related information that might be helpful."
        
        return response
    
    def _format_medium_confidence_response(self, best_result: Dict, search_results: Dict) -> str:
        """Format medium-confidence response."""
        content = best_result['text']
        
        if len(content) > 300:
            content = content[:300] + "..."
        
        return f"I found some information that might help:\n\n{content}\n\nWould you like me to search for something more specific?"
    
    def _format_low_confidence_response(self, best_result: Dict, search_results: Dict) -> str:
        """Format low-confidence response."""
        content = best_result['text']
        
        if len(content) > 250:
            content = content[:250] + "..."
        
        return f"{self.response_templates['low_confidence']}\n\n{content}\n\nIf this doesn't answer your question, please try rephrasing or ask about our menu, hours, or services."
    
    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Create standardized error response."""
        return {
            'response': self.response_templates['error'],
            'confidence': 0.0,
            'source_documents': [],
            'response_type': 'error',
            'error': error_msg,
            'timestamp': datetime.now().isoformat()
        }
    
    def _update_performance_metrics(self, response_time: float):
        """Update performance metrics."""
        total = self.performance_metrics['total_queries']
        current_avg = self.performance_metrics['avg_response_time']
        
        # Calculate new average response time
        new_avg = ((current_avg * (total - 1)) + response_time) / total
        self.performance_metrics['avg_response_time'] = new_avg
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        cache_hit_rate = 0
        if self.performance_metrics['total_queries'] > 0:
            cache_hit_rate = (self.performance_metrics['cache_hits'] / 
                            self.performance_metrics['total_queries']) * 100
        
        return {
            'total_queries': self.performance_metrics['total_queries'],
            'cache_hit_rate': f"{cache_hit_rate:.1f}%",
            'avg_response_time': f"{self.performance_metrics['avg_response_time']:.3f}s",
            'cache_hits': self.performance_metrics['cache_hits'],
            'uptime_since': self.performance_metrics['last_reset']
        }
    
    def clear_cache(self):
        """Clear response cache."""
        if self.cache:
            self.cache.cache = {}
            self.cache._save_cache()
            logger.info("Response cache cleared")
    
    def reset_metrics(self):
        """Reset performance metrics."""
        self.performance_metrics = {
            'total_queries': 0,
            'cache_hits': 0,
            'avg_response_time': 0,
            'last_reset': datetime.now().isoformat()
        }
        logger.info("Performance metrics reset")

# Global chatbot engine instance
_chatbot_engine = None

def get_chatbot_engine(pipeline=None) -> OptimizedChatbotEngine:
    """Get global chatbot engine instance."""
    global _chatbot_engine
    if _chatbot_engine is None:
        _chatbot_engine = OptimizedChatbotEngine(pipeline)
    elif pipeline and not _chatbot_engine.pipeline:
        _chatbot_engine.pipeline = pipeline
    return _chatbot_engine
