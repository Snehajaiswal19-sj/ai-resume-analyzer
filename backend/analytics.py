# backend/analytics.py

import json
import os
from datetime import datetime

class AnalyticsTracker:
    """Track resume score improvements over time"""
    
    def __init__(self):
        self.history_file = 'data/history.json'
        self.history = self.load_history()
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def add_analysis(self, score: float, skills_count: int, timestamp=None):
        """Add analysis to history"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        self.history.append({
            'score': score,
            'skills_count': skills_count,
            'timestamp': timestamp
        })
        
        # Save to file
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)
    
    def get_trends(self):
        """Get score trends"""
        if not self.history:
            return {'improvement': 0, 'average_score': 0, 'total_analyses': 0}
        
        scores = [h['score'] for h in self.history]
        
        return {
            'average_score': round(sum(scores) / len(scores), 2),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'total_analyses': len(self.history),
            'improvement': round(scores[-1] - scores[0], 2) if len(scores) > 1 else 0
        }