import re
from typing import Dict, List, Tuple

class ATSChecker:
    """Check resume ATS (Applicant Tracking System) compatibility"""
    
    def __init__(self):
        self.ats_keywords = {
            'contact_info': ['email', 'phone', 'address', 'linkedin'],
            'sections': ['experience', 'education', 'skills', 'projects', 'certifications'],
            'format': ['pdf', 'docx', 'txt'],
            'keywords': ['developed', 'managed', 'created', 'led', 'implemented', 'achieved']
        }
    
    def check_ats_compatibility(self, text: str, filename: str) -> Dict:
        """Check if resume is ATS friendly"""
        issues = []
        score = 100
        
        # Check for contact information
        if not re.search(r'[\w\.-]+@[\w\.-]+', text):
            issues.append({
                'severity': 'High',
                'issue': 'Email address not found',
                'fix': 'Add your email address in the resume header'
            })
            score -= 15
        
        if not re.search(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text):
            issues.append({
                'severity': 'High',
                'issue': 'Phone number not found',
                'fix': 'Add your phone number for recruiter contact'
            })
            score -= 10
        
        # Check for standard sections
        required_sections = {
            'experience': r'(?i)experience|employment|work history',
            'education': r'(?i)education|academic|qualification',
            'skills': r'(?i)skills|technical skills|competencies'
        }
        
        for section, pattern in required_sections.items():
            if not re.search(pattern, text):
                issues.append({
                    'severity': 'Medium',
                    'issue': f'Missing {section} section',
                    'fix': f'Add a clear {section} section with relevant details'
                })
                score -= 10
        
        # Check for tables or complex formatting
        if '\t' in text:
            issues.append({
                'severity': 'Medium',
                'issue': 'Tabs detected in resume',
                'fix': 'Use spaces instead of tabs, ATS may not parse tabs correctly'
            })
            score -= 5
        
        # Check for images or graphics
        if len(text.split()) < 100:
            issues.append({
                'severity': 'High',
                'issue': 'Resume is too short',
                'fix': 'Add more detail about your experience and projects'
            })
            score -= 20
        
        # Check for action verbs
        action_verbs = ['developed', 'created', 'managed', 'led', 'implemented', 'achieved']
        found_verbs = [verb for verb in action_verbs if verb in text.lower()]
        
        if len(found_verbs) < 3:
            issues.append({
                'severity': 'Low',
                'issue': 'Few action verbs found',
                'fix': 'Use action verbs like: developed, created, led, achieved'
            })
            score -= 10
        
        ats_score = max(0, min(score, 100))
        
        # ATS Rating
        if ats_score >= 90:
            rating = 'Excellent'
            color = 'success'
        elif ats_score >= 75:
            rating = 'Good'
            color = 'info'
        elif ats_score >= 60:
            rating = 'Average'
            color = 'warning'
        else:
            rating = 'Poor'
            color = 'danger'
        
        return {
            'ats_score': ats_score,
            'rating': rating,
            'color': color,
            'issues': issues,
            'passed': len([i for i in issues if i['severity'] == 'High']) == 0
        }