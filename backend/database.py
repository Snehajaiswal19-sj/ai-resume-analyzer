from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

class Database:
    """MongoDB Atlas database for production"""
    
    def __init__(self, connection_string=None):
        self.connection_string = connection_string or os.getenv('MONGODB_URI')
        
        if not self.connection_string:
            print("⚠️ MONGODB_URI not found!")
            self.client = None
            self.db = None
            return
        
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client['resume_analyzer']
            print("✅ MongoDB Atlas connected successfully!")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self.client = None
            self.db = None
    
    @property
    def users(self):
        return self.db['users'] if self.db is not None else None
    
    @property
    def analysis_history(self):
        return self.db['analysis_history'] if self.db is not None else None
    
    @property
    def bulk_analysis(self):
        return self.db['bulk_analysis'] if self.db is not None else None
    
    @property
    def career_roles(self):
        return self.db['career_roles'] if self.db is not None else None
    
    @property
    def certifications(self):
        return self.db['certifications'] if self.db is not None else None
    
    @property
    def cover_letters(self):
        return self.db['cover_letters'] if self.db is not None else None
    
    @property
    def resume_templates(self):
        return self.db['resume_templates'] if self.db is not None else None
    
    # User methods
    def create_user(self, email: str, name: str = None, password_hash: str = None) -> Dict:
        if self.users is None:
            return {'error': 'Database not connected'}
        
        user = {
            'email': email,
            'name': name,
            'password_hash': password_hash,
            'created_at': datetime.now()
        }
        
        existing = self.users.find_one({'email': email})
        if existing:
            return {'error': 'User already exists'}
        
        result = self.users.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user
    
    def get_user(self, email: str):
        if self.users is None:
            return None
        return self.users.find_one({'email': email})
    
    # Analysis methods
    def save_analysis(self, analysis_data: Dict) -> str:
        if self.analysis_history is None:
            return None
        
        analysis_data['created_at'] = datetime.now()
        result = self.analysis_history.insert_one(analysis_data)
        return str(result.inserted_id)
    
    def get_analysis_history(self, user_email: str = None, limit: int = 10) -> List[Dict]:
        if self.analysis_history is None:
            return []
        
        query = {}
        if user_email:
            query['user_email'] = user_email
        
        results = list(self.analysis_history.find(query).sort('created_at', -1).limit(limit))
        
        for result in results:
            result['_id'] = str(result['_id'])
        
        return results
    
    def get_stats(self, user_email: str = None) -> Dict:
        if self.analysis_history is None:
            return {
                'total_analyses': 0,
                'average_score': 0,
                'highest_score': 0,
                'total_users': 0
            }
        
        query = {}
        if user_email:
            query['user_email'] = user_email
        
        total_analyses = self.analysis_history.count_documents(query)
         # Count unique users from analysis history
        unique_users = len(self.analysis_history.distinct('user_email')) if total_analyses > 0 else 0
        
        pipeline = [
            {'$match': query},
            {'$group': {
                '_id': None,
                'avg_score': {'$avg': '$total_score'},
                'max_score': {'$max': '$total_score'}
            }}
        ]
        
        stats = list(self.analysis_history.aggregate(pipeline))
        
        if stats:
            return {
                'total_analyses': total_analyses,
                'average_score': round(stats[0]['avg_score'], 2),
                'highest_score': stats[0]['max_score'],
                'total_users': unique_users if unique_users > 0 else 1
            }
        
        return {
            'total_analyses': 0,
            'average_score': 0,
            'highest_score': 0,
            'total_users': 0
        }
    
    def save_bulk_analysis(self, batch_name: str, results: List[Dict], user_email: str = None) -> str:
        if self.bulk_analysis is None:
            return None
        
        bulk_data = {
            'batch_name': batch_name,
            'user_email': user_email,
            'total_files': len(results),
            'results': results,
            'created_at': datetime.now()
        }
        
        result = self.bulk_analysis.insert_one(bulk_data)
        return str(result.inserted_id)