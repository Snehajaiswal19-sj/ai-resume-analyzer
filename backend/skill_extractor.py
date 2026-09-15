import json
import re
from typing import List, Dict, Set
import spacy
from collections import Counter

class SkillExtractor:
    """Extract skills from resume text"""
    
    def __init__(self, skills_database_path='data/skills_database.json'):
        self.skills_database = self.load_skills_database(skills_database_path)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
    
    def load_skills_database(self, path: str) -> Dict:
        """Load skills from database"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default skills if database not found
            return {
                "technical_skills": [
                    "Python", "Java", "JavaScript", "C++", "C#", "SQL",
                    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
                    "React", "Node.js", "Django", "Flask", "Spring Boot",
                    "AWS", "Azure", "GCP", "Docker", "Kubernetes",
                    "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
                    "Pandas", "NumPy", "Matplotlib", "Seaborn",
                    "Git", "Linux", "REST API", "GraphQL", "MongoDB",
                    "PostgreSQL", "MySQL", "Redis", "Elasticsearch"
                ],
                "soft_skills": [
                    "Communication", "Leadership", "Team Management",
                    "Problem Solving", "Critical Thinking", "Time Management",
                    "Project Management", "Agile", "Scrum", "Collaboration",
                    "Adaptability", "Creativity", "Decision Making",
                    "Conflict Resolution", "Mentoring", "Public Speaking"
                ],
                "domain_skills": [
                    "Data Analysis", "Data Visualization", "Statistical Analysis",
                    "Business Intelligence", "Cloud Computing", "DevOps",
                    "Cybersecurity", "Blockchain", "IoT", "Robotics",
                    "Mobile Development", "Web Development", "Game Development",
                    "UI/UX Design", "Product Management", "Quality Assurance"
                ]
            }
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract all skills from resume text"""
        text_lower = text.lower()
        
        extracted_skills = {
            'technical_skills': [],
            'soft_skills': [],
            'domain_skills': []
        }
        
        for category, skills in self.skills_database.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    extracted_skills[category].append(skill)
        
        # Remove duplicates and sort
        for category in extracted_skills:
            extracted_skills[category] = sorted(list(set(extracted_skills[category])))
        
        return extracted_skills
    
    def extract_skills_with_context(self, text: str) -> List[Dict]:
        """Extract skills with context using NLP"""
        doc = self.nlp(text)
        skills_with_context = []
        
        for token in doc:
            if token.text in self.skills_database['technical_skills']:
                # Get surrounding context
                context = text[max(0, token.idx - 50):token.idx + len(token.text) + 50]
                skills_with_context.append({
                    'skill': token.text,
                    'context': context,
                    'position': token.idx
                })
        
        return skills_with_context
    
    def get_skill_frequency(self, text: str) -> Counter:
        """Get frequency of skills mentioned"""
        extracted = self.extract_skills(text)
        all_skills = [skill for skills in extracted.values() for skill in skills]
        return Counter(all_skills)
    
    def suggest_missing_skills(self, extracted_skills: Dict, job_role: str = None) -> List[str]:
        """Suggest skills that might be missing based on job role"""
        if not job_role:
            return []
        
        # Job role to required skills mapping
        role_skills_mapping = {
            'data scientist': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'TensorFlow'],
            'software engineer': ['Java', 'Python', 'Git', 'AWS', 'Agile'],
            'web developer': ['JavaScript', 'React', 'Node.js', 'HTML', 'CSS'],
            'devops engineer': ['Docker', 'Kubernetes', 'AWS', 'Linux', 'CI/CD'],
            'product manager': ['Product Management', 'Agile', 'Data Analysis', 'UI/UX']
        }
        
        job_role_lower = job_role.lower()
        if job_role_lower in role_skills_mapping:
            required_skills = role_skills_mapping[job_role_lower]
            current_skills = [s for skills in extracted_skills.values() for s in skills]
            missing = [skill for skill in required_skills if skill not in current_skills]
            return missing
        
        return []