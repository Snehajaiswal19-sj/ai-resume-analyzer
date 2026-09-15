import os
import pandas as pd
from typing import List, Dict
from werkzeug.utils import secure_filename
import uuid

class BulkAnalyzer:
    """Analyze multiple resumes at once"""
    
    def __init__(self, resume_parser, skill_extractor, score_calculator):
        self.resume_parser = resume_parser
        self.skill_extractor = skill_extractor
        self.score_calculator = score_calculator
    
    def analyze_bulk(self, files: List, upload_folder: str) -> List[Dict]:
        results = []
        
        for file in files:
            try:
                filename = secure_filename(file.filename)
                unique_name = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(upload_folder, unique_name)
                file.save(filepath)
                
                resume_text = self.resume_parser.extract_text(filepath)
                skills = self.skill_extractor.extract_skills(resume_text)
                scores = self.score_calculator.calculate_total_score(resume_text, skills)
                careers = self.score_calculator.predict_career_roles(resume_text, skills)
                
                results.append({
                    'filename': filename,
                    'total_score': scores['total_score'],
                    'grade': scores['grade'],
                    'skills_count': sum(len(s) for s in skills.values()),
                    'career_roles': careers[:2]
                })
                
                os.remove(filepath)
                
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'error': str(e)
                })
        
        return results
    
    def generate_excel(self, results: List[Dict], output_path: str) -> str:
        df = pd.DataFrame(results)
        # Flatten career_roles
        if 'career_roles' in df.columns:
            df['top_role'] = df['career_roles'].apply(lambda x: x[0]['role'] if x and len(x) > 0 else 'N/A')
            df.drop('career_roles', axis=1, inplace=True)
        df.to_excel(output_path, index=False)
        return output_path