"""
Enhanced Feedback Management System
Handles user feedback collection, storage, and analytics
Version: 1.0.0
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class FeedbackManager:
    """Professional feedback management system with separate storage for good/bad feedback."""
    
    def __init__(self, feedback_dir: str = "./feedback_data"):
        """Initialize feedback manager with storage directory."""
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(exist_ok=True)
        
        # Separate files for different feedback types
        self.good_feedback_file = self.feedback_dir / "good_feedback.jsonl"
        self.bad_feedback_file = self.feedback_dir / "bad_feedback.jsonl"
        self.analytics_file = self.feedback_dir / "feedback_analytics.json"
        
        # Initialize files if they don't exist
        self._initialize_files()
        
        logger.info(f"Feedback manager initialized with directory: {self.feedback_dir}")
    
    def _initialize_files(self):
        """Initialize feedback files if they don't exist."""
        for file_path in [self.good_feedback_file, self.bad_feedback_file]:
            if not file_path.exists():
                file_path.touch()
        
        if not self.analytics_file.exists():
            initial_analytics = {
                "total_feedback": 0,
                "good_feedback_count": 0,
                "bad_feedback_count": 0,
                "satisfaction_rate": 0.0,
                "last_updated": datetime.now().isoformat(),
                "common_issues": [],
                "top_queries": []
            }
            self._save_analytics(initial_analytics)
    
    def save_feedback(self, 
                     question: str, 
                     answer: str, 
                     feedback_type: str, 
                     user_comment: str = "",
                     metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Save user feedback to appropriate file.
        
        Args:
            question: The user's original question
            answer: The system's response
            feedback_type: 'good' or 'bad'
            user_comment: Optional user comment about the feedback
            metadata: Additional metadata (similarity scores, etc.)
        
        Returns:
            bool: True if saved successfully
        """
        try:
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "feedback_type": feedback_type,
                "user_comment": user_comment,
                "metadata": metadata or {},
                "session_id": self._generate_session_id()
            }
            
            # Choose appropriate file based on feedback type
            if feedback_type.lower() == 'good':
                target_file = self.good_feedback_file
            elif feedback_type.lower() == 'bad':
                target_file = self.bad_feedback_file
            else:
                logger.error(f"Invalid feedback type: {feedback_type}")
                return False
            
            # Append to JSONL file (one JSON object per line)
            with open(target_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(feedback_entry, ensure_ascii=False) + '\n')
            
            # Update analytics
            self._update_analytics(feedback_type)
            
            logger.info(f"Saved {feedback_type} feedback for question: {question[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")
            return False
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get summary of all feedback."""
        try:
            analytics = self._load_analytics()
            
            # Count current feedback
            good_count = self._count_feedback_entries(self.good_feedback_file)
            bad_count = self._count_feedback_entries(self.bad_feedback_file)
            total_count = good_count + bad_count
            
            satisfaction_rate = (good_count / total_count * 100) if total_count > 0 else 0
            
            return {
                "total_feedback": total_count,
                "good_feedback": good_count,
                "bad_feedback": bad_count,
                "satisfaction_rate": satisfaction_rate,
                "last_updated": datetime.now().isoformat(),
                "good_feedback_file": str(self.good_feedback_file),
                "bad_feedback_file": str(self.bad_feedback_file)
            }
            
        except Exception as e:
            logger.error(f"Failed to get feedback summary: {e}")
            return {}
    
    def get_recent_feedback(self, feedback_type: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent feedback entries."""
        try:
            feedback_entries = []
            
            files_to_read = []
            if feedback_type.lower() in ['all', 'good']:
                files_to_read.append(self.good_feedback_file)
            if feedback_type.lower() in ['all', 'bad']:
                files_to_read.append(self.bad_feedback_file)
            
            for file_path in files_to_read:
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Get last 'limit' lines
                        recent_lines = lines[-limit:] if len(lines) > limit else lines
                        
                        for line in recent_lines:
                            try:
                                entry = json.loads(line.strip())
                                feedback_entries.append(entry)
                            except json.JSONDecodeError:
                                continue
            
            # Sort by timestamp (most recent first)
            feedback_entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return feedback_entries[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get recent feedback: {e}")
            return []
    
    def analyze_bad_feedback(self) -> Dict[str, Any]:
        """Analyze bad feedback to identify common issues."""
        try:
            bad_feedback = self.get_recent_feedback('bad', limit=100)
            
            if not bad_feedback:
                return {"message": "No bad feedback found"}
            
            # Analyze common patterns
            common_issues = {}
            question_types = {}
            
            for entry in bad_feedback:
                question = entry.get('question', '').lower()
                comment = entry.get('user_comment', '').lower()
                
                # Simple keyword analysis
                keywords = ['error', 'wrong', 'incorrect', 'bad', 'poor', 'useless', 'unhelpful']
                for keyword in keywords:
                    if keyword in comment:
                        common_issues[keyword] = common_issues.get(keyword, 0) + 1
                
                # Question type analysis
                if question.startswith('what'):
                    question_types['what'] = question_types.get('what', 0) + 1
                elif question.startswith('how'):
                    question_types['how'] = question_types.get('how', 0) + 1
                elif question.startswith('where'):
                    question_types['where'] = question_types.get('where', 0) + 1
            
            return {
                "total_bad_feedback": len(bad_feedback),
                "common_issues": dict(sorted(common_issues.items(), key=lambda x: x[1], reverse=True)),
                "question_types": dict(sorted(question_types.items(), key=lambda x: x[1], reverse=True)),
                "analysis_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze bad feedback: {e}")
            return {"error": str(e)}
    
    def export_feedback(self, output_file: str, feedback_type: str = "all") -> bool:
        """Export feedback to a readable format."""
        try:
            feedback_data = self.get_recent_feedback(feedback_type, limit=1000)
            
            export_data = {
                "export_date": datetime.now().isoformat(),
                "feedback_type": feedback_type,
                "total_entries": len(feedback_data),
                "feedback_entries": feedback_data
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(feedback_data)} feedback entries to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export feedback: {e}")
            return False
    
    def _count_feedback_entries(self, file_path: Path) -> int:
        """Count number of feedback entries in a file."""
        try:
            if not file_path.exists():
                return 0
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0
    
    def _generate_session_id(self) -> str:
        """Generate a simple session ID based on timestamp."""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _update_analytics(self, feedback_type: str):
        """Update analytics after new feedback."""
        try:
            analytics = self._load_analytics()
            
            analytics['total_feedback'] += 1
            if feedback_type.lower() == 'good':
                analytics['good_feedback_count'] += 1
            else:
                analytics['bad_feedback_count'] += 1
            
            # Recalculate satisfaction rate
            total = analytics['total_feedback']
            good = analytics['good_feedback_count']
            analytics['satisfaction_rate'] = (good / total * 100) if total > 0 else 0
            analytics['last_updated'] = datetime.now().isoformat()
            
            self._save_analytics(analytics)
            
        except Exception as e:
            logger.error(f"Failed to update analytics: {e}")
    
    def _load_analytics(self) -> Dict[str, Any]:
        """Load analytics from file."""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load analytics: {e}")
        
        # Return default analytics if loading fails
        return {
            "total_feedback": 0,
            "good_feedback_count": 0,
            "bad_feedback_count": 0,
            "satisfaction_rate": 0.0,
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_analytics(self, analytics: Dict[str, Any]):
        """Save analytics to file."""
        try:
            with open(self.analytics_file, 'w', encoding='utf-8') as f:
                json.dump(analytics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save analytics: {e}")

# Global feedback manager instance
_feedback_manager = None

def get_feedback_manager() -> FeedbackManager:
    """Get global feedback manager instance."""
    global _feedback_manager
    if _feedback_manager is None:
        _feedback_manager = FeedbackManager()
    return _feedback_manager
