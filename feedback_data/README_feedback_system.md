# 📊 Feedback System Files

This directory contains all user feedback data collected by the enhanced feedback system.

## 📁 File Structure

```
feedback_data/
├── good_feedback.jsonl      # All positive feedback entries
├── bad_feedback.jsonl       # All negative feedback entries
├── feedback_analytics.json  # Real-time statistics and analytics
└── README_feedback_system.md # This documentation file
```

## 📄 File Descriptions

### `good_feedback.jsonl`
- Contains all positive feedback (👍 Helpful responses)
- Each line is a separate JSON object with question, answer, and user comments
- Automatically created when first positive feedback is submitted

### `bad_feedback.jsonl`
- Contains all negative feedback (👎 Not Helpful responses)
- Each line is a separate JSON object with question, answer, and user comments
- Automatically created when first negative feedback is submitted

### `feedback_analytics.json`
- Contains summary statistics and analytics
- Updated in real-time as feedback is collected
- Includes satisfaction rates, common issues, and trends

## 🔍 Sample Feedback Entry Format

```json
{
  "timestamp": "2025-09-19T05:02:00",
  "question": "What are your opening hours?",
  "answer": "We are open Monday-Friday 9AM-9PM, Saturday 10AM-8PM, closed Sunday.",
  "feedback_type": "good",
  "user_comment": "Very helpful and accurate information!",
  "metadata": {
    "similarity_score": 0.85,
    "response_id": 2,
    "timestamp": "05:02"
  },
  "session_id": "session_20250919_050200"
}
```

## 📈 How to Use the Feedback Data

1. **View Feedback**: Open `.jsonl` files in any text editor
2. **Analyze Patterns**: Use the analytics features in the GUI
3. **Export Data**: Use the feedback manager's export functionality
4. **Improve Responses**: Review bad feedback to identify areas for improvement

## 🔧 Accessing Feedback Programmatically

```python
from core.feedback_manager import get_feedback_manager

# Get feedback manager
feedback_manager = get_feedback_manager()

# Get summary statistics
summary = feedback_manager.get_feedback_summary()
print(f"Total feedback: {summary['total_feedback']}")
print(f"Satisfaction rate: {summary['satisfaction_rate']:.1f}%")

# Get recent feedback
recent_feedback = feedback_manager.get_recent_feedback('all', limit=10)
for entry in recent_feedback:
    print(f"Q: {entry['question']}")
    print(f"A: {entry['answer']}")
    print(f"Feedback: {entry['feedback_type']}")
    print("---")
```

## 📊 Analytics Features

The feedback system provides:
- Real-time satisfaction rate calculation
- Common issue identification from negative feedback
- Question type analysis
- Export capabilities for external analysis
- Trend tracking over time

Files are automatically created when users first provide feedback through the GUI application.
