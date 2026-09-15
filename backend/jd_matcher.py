import re
from typing import Dict, List, Tuple
from collections import Counter

class JDMatcher:
    """Match resume with job description"""
    
    def __init__(self):
        self.importance_weights = {
            'skills': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'keywords': 0.1
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Remove common words and extract keywords
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords
    
    def match_with_jd(self, resume_text: str, jd_text: str) -> Dict:
        """Calculate match percentage between resume and job description"""
        
        # Extract keywords
        resume_keywords = set(self.extract_keywords(resume_text))
        jd_keywords = set(self.extract_keywords(jd_text))
        
        # Find matching keywords
        matching_keywords = resume_keywords.intersection(jd_keywords)
        missing_keywords = jd_keywords - resume_keywords
        
        # Calculate match percentage
        if len(jd_keywords) > 0:
            keyword_match = len(matching_keywords) / len(jd_keywords) * 100
        else:
            keyword_match = 0
        
        # Extract skills from JD
        skills_pattern = r'(?i)skills?[:\s]+(.+?)(?:\n|$)'
        skills_match = re.search(skills_pattern, jd_text)
        jd_skills = []
        if skills_match:
            jd_skills = [s.strip() for s in re.split(r'[,;]', skills_match.group(1)) if s.strip()]
        
        # Match skills
        resume_skills = self.extract_keywords(resume_text)
        matching_skills = [s for s in jd_skills if s.lower() in resume_text.lower()]
        missing_skills = [s for s in jd_skills if s.lower() not in resume_text.lower()]
        
        skill_match = (len(matching_skills) / len(jd_skills) * 100) if jd_skills else 0
        
        # Overall match
        overall_match = (keyword_match * 0.6 + skill_match * 0.4)
        
        # Generate recommendations
        recommendations = []
        
        if missing_skills:
            recommendations.append({
                'category': 'Skills Gap',
                'suggestion': f'Add these skills to your resume: {", ".join(missing_skills[:5])}',
                'priority': 'High'
            })
        
        if overall_match < 50:
            recommendations.append({
                'category': 'Overall Match',
                'suggestion': 'Resume does not closely match this job description. Tailor your resume.',
                'priority': 'High'
            })
        elif overall_match < 75:
            recommendations.append({
                'category': 'Overall Match',
                'suggestion': 'Resume partially matches. Add more relevant keywords from JD.',
                'priority': 'Medium'
            })
        
        return {
            'overall_match': round(overall_match, 2),
            'keyword_match': round(keyword_match, 2),
            'skill_match': round(skill_match, 2),
            'matching_keywords': list(matching_keywords)[:10],
            'missing_keywords': list(missing_keywords)[:10],
            'matching_skills': matching_skills,
            'missing_skills': missing_skills[:10],
            'recommendations': recommendations
        }