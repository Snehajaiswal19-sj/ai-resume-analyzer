import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import re
from typing import Dict, List

class MLScorePredictor:
    """Advanced ML model for resume score prediction"""
    
    def __init__(self):
        self.model = None
        self.model_path = 'models/score_predictor.pkl'
        self.feature_names = [
            'word_count', 'skills_count', 'technical_skills', 'soft_skills',
            'domain_skills', 'experience_years', 'education_level',
            'has_email', 'has_phone', 'action_verbs', 'projects_count',
            'certifications_count', 'achievements_count'
        ]
    
    def extract_features(self, resume_text: str, extracted_skills: Dict) -> np.ndarray:
        """Extract comprehensive features"""
        features = []
        
        # Text features
        word_count = len(resume_text.split())
        features.append(word_count)
        
        # Skills
        total_skills = sum(len(skills) for skills in extracted_skills.values())
        features.append(total_skills)
        features.append(len(extracted_skills.get('technical_skills', [])))
        features.append(len(extracted_skills.get('soft_skills', [])))
        features.append(len(extracted_skills.get('domain_skills', [])))
        
        # Experience
        exp_match = re.search(r'(\d+)\s*\+?\s*years?', resume_text, re.IGNORECASE)
        features.append(int(exp_match.group(1)) if exp_match else 0)
        
        # Education
        text_lower = resume_text.lower()
        if 'phd' in text_lower or 'doctorate' in text_lower:
            education = 100
        elif 'master' in text_lower or 'mba' in text_lower:
            education = 80
        elif 'bachelor' in text_lower or 'b.tech' in text_lower:
            education = 60
        elif 'diploma' in text_lower:
            education = 40
        else:
            education = 20
        features.append(education)
        
        # Contact info
        features.append(1 if '@' in resume_text else 0)
        features.append(1 if re.search(r'\d{10}', resume_text) else 0)
        
        # Action verbs
        action_verbs = ['developed', 'created', 'managed', 'led', 'implemented',
                       'designed', 'improved', 'achieved', 'launched', 'built']
        features.append(sum(1 for v in action_verbs if v in text_lower))
        
        # Projects
        features.append(len(re.findall(r'(?i)project', resume_text)))
        
        # Certifications
        features.append(len(re.findall(r'(?i)certification|certificate', resume_text)))
        
        # Achievements with numbers
        features.append(len(re.findall(r'\d+%|\d+\s*(?:users|customers|clients|revenue)', resume_text)))
        
        return np.array(features).reshape(1, -1)
    
    def train_model(self, X: np.ndarray, y: np.ndarray):
        """Train the ML model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        
        return {
            'mse': mse,
            'r2': r2,
            'accuracy': r2 * 100
        }
    
    def predict_score(self, resume_text: str, extracted_skills: Dict) -> Dict:
        """Predict resume score"""
        features = self.extract_features(resume_text, extracted_skills)
        
        # Load model if exists
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            predicted_score = float(self.model.predict(features)[0])
        else:
            # Fallback: weighted scoring
            predicted_score = self._fallback_score(features[0])
        
        # Calculate confidence
        confidence = self._calculate_confidence(features[0])
        
        return {
            'ml_score': round(min(max(predicted_score, 0), 100), 2),
            'confidence': confidence,
            'feature_importance': self._get_feature_importance(features[0])
        }
    
    def _fallback_score(self, features: np.ndarray) -> float:
        """Fallback scoring method"""
        weights = [0.1, 0.15, 0.1, 0.05, 0.05, 0.15, 0.1, 0.05, 0.05, 0.1, 0.05, 0.03, 0.02]
        return float(np.dot(features, weights))
    
    def _calculate_confidence(self, features: np.ndarray) -> str:
        """Calculate confidence level"""
        total_signals = sum(1 for f in features if f > 0)
        if total_signals >= 10:
            return 'High'
        elif total_signals >= 7:
            return 'Medium'
        else:
            return 'Low'
    
    def _get_feature_importance(self, features: np.ndarray) -> Dict:
        """Get feature importance"""
        importance = {}
        for name, value in zip(self.feature_names, features):
            importance[name] = int(value)
        return importance