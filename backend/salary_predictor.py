from typing import Dict, List
import re

class SalaryPredictor:
    """Predict salary based on role, skills, and experience"""
    
    def __init__(self):
        self.salary_data = {
            "Data Scientist": {
                "entry": 800000, "mid": 1500000, "senior": 3000000,
                "high_demand_skills": ["Deep Learning", "NLP", "TensorFlow", "PyTorch"],
                "bonus_per_skill": 100000
            },
            "Software Engineer": {
                "entry": 500000, "mid": 1200000, "senior": 2500000,
                "high_demand_skills": ["Java", "Python", "AWS", "Docker", "Kubernetes"],
                "bonus_per_skill": 50000
            },
            "Web Developer": {
                "entry": 300000, "mid": 800000, "senior": 1800000,
                "high_demand_skills": ["React", "Node.js", "TypeScript", "MongoDB"],
                "bonus_per_skill": 40000
            },
            "DevOps Engineer": {
                "entry": 600000, "mid": 1500000, "senior": 2800000,
                "high_demand_skills": ["Docker", "Kubernetes", "AWS", "Terraform"],
                "bonus_per_skill": 60000
            },
            "Business Analyst": {
                "entry": 400000, "mid": 1000000, "senior": 2000000,
                "high_demand_skills": ["SQL", "Power BI", "Tableau", "Excel"],
                "bonus_per_skill": 30000
            },
            "UI/UX Designer": {
                "entry": 350000, "mid": 900000, "senior": 2000000,
                "high_demand_skills": ["Figma", "Adobe XD", "Sketch", "Prototyping"],
                "bonus_per_skill": 30000
            },
            "Product Manager": {
                "entry": 800000, "mid": 1800000, "senior": 3500000,
                "high_demand_skills": ["Product Management", "Agile", "Data Analysis"],
                "bonus_per_skill": 70000
            }
        }
        
        self.location_multipliers = {
            "bangalore": 1.3, "mumbai": 1.25, "delhi": 1.2,
            "hyderabad": 1.15, "pune": 1.1, "chennai": 1.05,
            "remote": 1.0, "other": 0.9
        }
    
    def predict_salary(self, role: str, experience_years: int, skills: List[str], 
                      location: str = 'remote') -> Dict:
        """Predict salary range"""
        if role not in self.salary_data:
            role = "Software Engineer"
        
        data = self.salary_data[role]
        
        # Base salary based on experience
        if experience_years <= 2:
            base_salary = data['entry']
            level = 'Entry Level'
        elif experience_years <= 5:
            base_salary = data['mid']
            level = 'Mid Level'
        else:
            base_salary = data['senior']
            level = 'Senior Level'
        
        # Skill bonus
        matching_skills = [s for s in skills if s in data['high_demand_skills']]
        skill_bonus = len(matching_skills) * data['bonus_per_skill']
        
        # Location adjustment
        location_key = location.lower() if location else 'remote'
        location_multiplier = self.location_multipliers.get(location_key, 1.0)
        
        # Calculate salary ranges
        min_salary = base_salary * location_multiplier
        max_salary = (base_salary + skill_bonus) * location_multiplier
        average_salary = (min_salary + max_salary) / 2
        
        # Format in LPA (Lakhs Per Annum)
        return {
            'level': level,
            'min_lpa': round(min_salary / 100000, 1),
            'max_lpa': round(max_salary / 100000, 1),
            'average_lpa': round(average_salary / 100000, 1),
            'matching_skills': matching_skills,
            'currency': 'INR',
            'location': location
        }