from typing import Dict, List, Tuple
import re
from collections import Counter

class ScoreCalculator:
    """Calculate resume score based on various factors"""
    
    def __init__(self):
        self.weights = {
            'skills': 30,
            'experience': 25,
            'education': 20,
            'formatting': 15,
            'keyword': 10
        }
        
        # Comprehensive career database with 50+ professions
        self.career_database = {
            # Tech Roles
            "Data Scientist": {
                "skills": ["Python", "Machine Learning", "Data Analysis", "Statistics", "SQL", "TensorFlow", "Deep Learning", "Pandas", "NumPy", "NLP"],
                "keywords": ["data", "machine learning", "model", "analysis", "prediction", "AI", "statistics", "visualization"],
                "education": ["bachelor", "master", "phd", "computer science", "statistics", "mathematics"]
            },
            "Software Engineer": {
                "skills": ["Java", "Python", "C++", "JavaScript", "Git", "SQL", "AWS", "Docker", "REST API", "Microservices", "Agile"],
                "keywords": ["software", "development", "code", "application", "backend", "frontend", "programming"],
                "education": ["bachelor", "master", "computer science", "software engineering"]
            },
            "Web Developer": {
                "skills": ["JavaScript", "React", "Node.js", "HTML", "CSS", "Django", "Flask", "TypeScript", "Angular", "Vue.js", "MongoDB"],
                "keywords": ["web", "frontend", "backend", "fullstack", "website", "UI", "responsive"],
                "education": ["bachelor", "diploma", "computer science", "web development"]
            },
            "DevOps Engineer": {
                "skills": ["Docker", "Kubernetes", "AWS", "Azure", "Linux", "CI/CD", "Jenkins", "Git", "Python", "Terraform", "Ansible"],
                "keywords": ["deployment", "infrastructure", "automation", "cloud", "server", "pipeline"],
                "education": ["bachelor", "master", "computer science", "IT"]
            },
            "Cybersecurity Analyst": {
                "skills": ["Network Security", "Python", "Linux", "Firewall", "Penetration Testing", "SIEM", "Cryptography", "Risk Assessment"],
                "keywords": ["security", "cyber", "threat", "vulnerability", "firewall", "encryption"],
                "education": ["bachelor", "master", "cybersecurity", "computer science"]
            },
            "Cloud Architect": {
                "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux", "Networking"],
                "keywords": ["cloud", "architecture", "infrastructure", "migration", "scalable"],
                "education": ["bachelor", "master", "cloud computing", "IT"]
            },
            "Mobile App Developer": {
                "skills": ["Android", "iOS", "Flutter", "React Native", "Kotlin", "Swift", "Java", "Firebase"],
                "keywords": ["mobile", "app", "android", "ios", "flutter", "react native"],
                "education": ["bachelor", "diploma", "computer science"]
            },
            "AI Engineer": {
                "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Neural Networks"],
                "keywords": ["AI", "artificial intelligence", "neural", "deep learning", "model"],
                "education": ["master", "phd", "computer science", "AI"]
            },
            "Data Analyst": {
                "skills": ["SQL", "Excel", "Python", "Tableau", "Power BI", "Data Visualization", "Statistics"],
                "keywords": ["data", "analysis", "visualization", "dashboard", "insights"],
                "education": ["bachelor", "master", "statistics", "mathematics", "computer science"]
            },
            
            # Business & Finance
            "Chartered Accountant (CA)": {
                "skills": ["Accounting", "Taxation", "Auditing", "Financial Reporting", "GST", "Tally", "Excel", "Compliance", "Finance", "Balance Sheet"],
                "keywords": ["accounting", "tax", "audit", "financial", "balance sheet", "GST", "compliance", "ledger"],
                "education": ["bachelor", "chartered accountancy", "commerce", "accounting", "CA", "B.Com"]
            },
            "Financial Analyst": {
                "skills": ["Financial Analysis", "Excel", "Financial Modeling", "Valuation", "SQL", "Power BI", "Forecasting"],
                "keywords": ["financial", "analysis", "investment", "valuation", "budget", "forecast"],
                "education": ["bachelor", "master", "finance", "commerce", "economics"]
            },
            "Investment Banker": {
                "skills": ["Financial Modeling", "Valuation", "M&A", "Excel", "PowerPoint", "Due Diligence"],
                "keywords": ["investment", "banking", "M&A", "valuation", "deal", "capital"],
                "education": ["bachelor", "master", "finance", "MBA"]
            },
            "Business Analyst": {
                "skills": ["Data Analysis", "SQL", "Excel", "Power BI", "Tableau", "Communication", "Requirements Gathering", "Process Improvement"],
                "keywords": ["business", "requirements", "stakeholder", "analysis", "process"],
                "education": ["bachelor", "master", "business", "management"]
            },
            "Marketing Manager": {
                "skills": ["Digital Marketing", "SEO", "Social Media", "Content Strategy", "Google Analytics", "Brand Management"],
                "keywords": ["marketing", "campaign", "brand", "SEO", "social media", "advertising"],
                "education": ["bachelor", "master", "marketing", "MBA"]
            },
            "HR Manager": {
                "skills": ["Recruitment", "Employee Relations", "HR Policies", "Performance Management", "Communication", "Payroll"],
                "keywords": ["HR", "recruitment", "employee", "hiring", "talent", "compensation"],
                "education": ["bachelor", "master", "HR", "MBA"]
            },
            "Product Manager": {
                "skills": ["Product Management", "Agile", "Scrum", "Data Analysis", "Communication", "Leadership", "Market Research", "Roadmapping"],
                "keywords": ["product", "roadmap", "strategy", "user", "market", "stakeholder"],
                "education": ["bachelor", "master", "MBA", "management"]
            },
            "Entrepreneur": {
                "skills": ["Business Planning", "Leadership", "Marketing", "Finance", "Communication", "Innovation"],
                "keywords": ["startup", "business", "entrepreneur", "venture", "innovation"],
                "education": ["bachelor", "master", "MBA", "business"]
            },
            "Digital Marketer": {
                "skills": ["SEO", "SEM", "Social Media Marketing", "Google Ads", "Content Marketing", "Email Marketing"],
                "keywords": ["digital", "marketing", "SEO", "social media", "campaign", "ads"],
                "education": ["bachelor", "diploma", "marketing"]
            },
            "Sales Manager": {
                "skills": ["Sales", "Negotiation", "CRM", "Lead Generation", "Communication", "Team Management"],
                "keywords": ["sales", "revenue", "client", "negotiation", "target"],
                "education": ["bachelor", "master", "MBA", "business"]
            },
            
            # Creative Roles
            "UI/UX Designer": {
                "skills": ["UI/UX Design", "Figma", "Adobe XD", "Sketch", "Wireframing", "Prototyping", "HTML", "CSS", "User Research"],
                "keywords": ["design", "user experience", "interface", "prototype", "wireframe", "UX"],
                "education": ["bachelor", "diploma", "design"]
            },
            "Graphic Designer": {
                "skills": ["Photoshop", "Illustrator", "InDesign", "Typography", "Branding", "Logo Design", "Color Theory"],
                "keywords": ["design", "graphic", "logo", "brand", "creative", "visual"],
                "education": ["bachelor", "diploma", "design", "fine arts"]
            },
            "Makeup Artist": {
                "skills": ["Makeup Application", "Bridal Makeup", "Fashion Makeup", "Skin Care", "Color Theory", "Client Communication"],
                "keywords": ["makeup", "beauty", "bridal", "fashion", "cosmetics", "skincare"],
                "education": ["diploma", "certification", "cosmetology", "beauty"]
            },
            "Photographer": {
                "skills": ["Photography", "Photoshop", "Lightroom", "Lighting", "Composition", "Video Editing"],
                "keywords": ["photography", "photo", "camera", "shoot", "editing", "visual"],
                "education": ["diploma", "bachelor", "photography", "fine arts"]
            },
            "Content Writer": {
                "skills": ["Writing", "SEO Writing", "Copywriting", "Content Strategy", "Editing", "Research"],
                "keywords": ["content", "writing", "blog", "article", "copy", "SEO"],
                "education": ["bachelor", "master", "english", "journalism", "communications"]
            },
            "Video Editor": {
                "skills": ["Premiere Pro", "After Effects", "Final Cut Pro", "Color Grading", "Motion Graphics"],
                "keywords": ["video", "editing", "post-production", "motion", "animation"],
                "education": ["diploma", "bachelor", "film", "media"]
            },
            "Fashion Designer": {
                "skills": ["Fashion Design", "Illustration", "Pattern Making", "Textile Knowledge", "Trend Analysis"],
                "keywords": ["fashion", "design", "clothing", "apparel", "style"],
                "education": ["bachelor", "diploma", "fashion design"]
            },
            "Interior Designer": {
                "skills": ["Interior Design", "AutoCAD", "3D Modeling", "Space Planning", "Color Theory"],
                "keywords": ["interior", "design", "space", "furniture", "decor"],
                "education": ["bachelor", "diploma", "interior design"]
            },
            "Event Manager": {
                "skills": ["Event Planning", "Vendor Management", "Budgeting", "Communication", "Coordination"],
                "keywords": ["event", "planning", "coordination", "venue", "management"],
                "education": ["bachelor", "diploma", "event management", "hospitality"]
            },
            
            # Medical & Healthcare
            "Doctor": {
                "skills": ["Patient Care", "Medical Diagnosis", "Treatment Planning", "Clinical Skills", "Medical Knowledge", "Communication"],
                "keywords": ["medical", "patient", "clinical", "diagnosis", "treatment", "healthcare"],
                "education": ["MBBS", "MD", "MS", "medical", "bachelor of medicine"]
            },
            "Nurse": {
                "skills": ["Patient Care", "Medication Administration", "Clinical Skills", "Communication", "Emergency Care"],
                "keywords": ["nursing", "patient", "care", "clinical", "healthcare"],
                "education": ["bachelor", "diploma", "nursing", "healthcare"]
            },
            "Pharmacist": {
                "skills": ["Pharmaceutical Knowledge", "Prescription Processing", "Patient Counseling", "Inventory Management"],
                "keywords": ["pharmacy", "medicine", "drug", "prescription", "pharmaceutical"],
                "education": ["bachelor", "master", "pharmacy"]
            },
            
            # Legal
            "Lawyer": {
                "skills": ["Legal Research", "Litigation", "Contract Law", "Legal Writing", "Negotiation", "Client Counseling"],
                "keywords": ["legal", "law", "court", "litigation", "contract", "case"],
                "education": ["bachelor", "LLB", "LLM", "law"]
            },
            
            # Engineering
            "Civil Engineer": {
                "skills": ["AutoCAD", "Structural Analysis", "Construction Management", "Surveying", "Project Planning"],
                "keywords": ["civil", "construction", "structural", "building", "infrastructure"],
                "education": ["bachelor", "master", "civil engineering"]
            },
            "Mechanical Engineer": {
                "skills": ["AutoCAD", "SolidWorks", "Thermodynamics", "Machine Design", "Manufacturing"],
                "keywords": ["mechanical", "machine", "manufacturing", "design", "engineering"],
                "education": ["bachelor", "master", "mechanical engineering"]
            },
            "Electrical Engineer": {
                "skills": ["Circuit Design", "Power Systems", "PCB Design", "PLC", "Electrical Safety"],
                "keywords": ["electrical", "circuit", "power", "electronics", "engineering"],
                "education": ["bachelor", "master", "electrical engineering"]
            },
            
            # Education
            "Teacher": {
                "skills": ["Teaching", "Lesson Planning", "Communication", "Classroom Management", "Curriculum Development"],
                "keywords": ["teaching", "education", "student", "classroom", "lesson"],
                "education": ["bachelor", "master", "B.Ed", "education"]
            },
            "Professor": {
                "skills": ["Teaching", "Research", "Academic Writing", "Mentoring", "Publication"],
                "keywords": ["academic", "research", "teaching", "publication", "university"],
                "education": ["phd", "master", "doctorate"]
            },
            
            # Other Professions
            "Chef": {
                "skills": ["Cooking", "Menu Planning", "Food Safety", "Kitchen Management", "Recipe Development"],
                "keywords": ["cooking", "food", "kitchen", "culinary", "recipe"],
                "education": ["diploma", "bachelor", "culinary arts", "hotel management"]
            },
            "Architect": {
                "skills": ["AutoCAD", "3D Modeling", "Building Design", "SketchUp", "Construction Knowledge"],
                "keywords": ["architecture", "design", "building", "construction", "planning"],
                "education": ["bachelor", "master", "architecture"]
            },
            "Sports Coach": {
                "skills": ["Coaching", "Training", "Physical Fitness", "Motivation", "Team Management"],
                "keywords": ["sports", "coaching", "training", "fitness", "athlete"],
                "education": ["bachelor", "diploma", "sports", "physical education"]
            },
            "Journalist": {
                "skills": ["Writing", "Reporting", "Editing", "Research", "Communication", "Storytelling"],
                "keywords": ["journalism", "news", "reporting", "writing", "media"],
                "education": ["bachelor", "master", "journalism", "mass communication"]
            },
            "Psychologist": {
                "skills": ["Counseling", "Psychological Assessment", "Therapy", "Communication", "Research"],
                "keywords": ["psychology", "counseling", "therapy", "mental health", "behavior"],
                "education": ["bachelor", "master", "phd", "psychology"]
            },
            "Social Worker": {
                "skills": ["Counseling", "Community Development", "Communication", "Case Management"],
                "keywords": ["social", "community", "welfare", "counseling", "support"],
                "education": ["bachelor", "master", "social work"]
            }
        }
        
        # Role mapping for flexible matching
        self.role_mapping = {
            "ca": "Chartered Accountant (CA)",
            "chartered accountant": "Chartered Accountant (CA)",
            "chartered accountancy": "Chartered Accountant (CA)",
            "accountant": "Chartered Accountant (CA)",
            "ds": "Data Scientist",
            "data scientist": "Data Scientist",
            "data science": "Data Scientist",
            "sde": "Software Engineer",
            "software engineer": "Software Engineer",
            "software developer": "Software Engineer",
            "web dev": "Web Developer",
            "web developer": "Web Developer",
            "full stack": "Web Developer",
            "devops": "DevOps Engineer",
            "devops engineer": "DevOps Engineer",
            "doctor": "Doctor",
            "medical": "Doctor",
            "physician": "Doctor",
            "lawyer": "Lawyer",
            "legal": "Lawyer",
            "teacher": "Teacher",
            "educator": "Teacher",
            "professor": "Professor",
            "makeup": "Makeup Artist",
            "makeup artist": "Makeup Artist",
            "beauty": "Makeup Artist",
            "designer": "Graphic Designer",
            "graphic designer": "Graphic Designer",
            "ui/ux": "UI/UX Designer",
            "ux designer": "UI/UX Designer",
            "ui designer": "UI/UX Designer",
            "photographer": "Photographer",
            "chef": "Chef",
            "cook": "Chef",
            "nurse": "Nurse",
            "pharmacist": "Pharmacist",
            "architect": "Architect",
            "civil engineer": "Civil Engineer",
            "mechanical engineer": "Mechanical Engineer",
            "electrical engineer": "Electrical Engineer",
            "hr": "HR Manager",
            "hr manager": "HR Manager",
            "marketing": "Marketing Manager",
            "marketing manager": "Marketing Manager",
            "product manager": "Product Manager",
            "pm": "Product Manager",
            "business analyst": "Business Analyst",
            "ba": "Business Analyst",
            "financial analyst": "Financial Analyst",
            "investment banker": "Investment Banker",
            "data analyst": "Data Analyst",
            "digital marketer": "Digital Marketer",
            "sales manager": "Sales Manager",
            "content writer": "Content Writer",
            "video editor": "Video Editor",
            "fashion designer": "Fashion Designer",
            "interior designer": "Interior Designer",
            "event manager": "Event Manager",
            "sports coach": "Sports Coach",
            "journalist": "Journalist",
            "psychologist": "Psychologist",
            "social worker": "Social Worker",
            "cybersecurity": "Cybersecurity Analyst",
            "cloud architect": "Cloud Architect",
            "mobile developer": "Mobile App Developer",
            "ai engineer": "AI Engineer",
            "entrepreneur": "Entrepreneur"
        }
    
    def calculate_total_score(self, resume_text: str, extracted_skills: Dict) -> Dict:
        """Calculate overall resume score"""
        scores = {
            'skills_score': self.calculate_skills_score(extracted_skills),
            'experience_score': self.calculate_experience_score(resume_text),
            'education_score': self.calculate_education_score(resume_text),
            'formatting_score': self.calculate_formatting_score(resume_text),
            'keyword_score': self.calculate_keyword_score(resume_text)
        }
        
        total_score = sum(
            scores[f'{key}_score'] * weight / 100 
            for key, weight in self.weights.items()
        )
        
        scores['total_score'] = round(min(total_score, 100), 2)
        scores['grade'] = self.get_grade(scores['total_score'])
        
        return scores
    
    def calculate_skills_score(self, extracted_skills: Dict) -> float:
        total_skills = sum(len(skills) for skills in extracted_skills.values() if isinstance(skills, list))
        
        if total_skills >= 20:
            return 100
        elif total_skills >= 15:
            return 85
        elif total_skills >= 10:
            return 70
        elif total_skills >= 5:
            return 50
        else:
            return 30
    
    def calculate_experience_score(self, text: str) -> float:
        experience_patterns = [
            r'(\d+)\s*\+?\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?',
            r'experience[:\s]+(\d+)'
        ]
        
        max_years = 0
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    years = max(int(match[0]), int(match[1]))
                else:
                    years = int(match)
                max_years = max(max_years, years)
        
        if max_years >= 10:
            return 100
        elif max_years >= 5:
            return 85
        elif max_years >= 3:
            return 70
        elif max_years >= 1:
            return 50
        else:
            return 20
    
    def calculate_education_score(self, text: str) -> float:
        education_keywords = {
            'phd': 100, 'doctorate': 100, 'masters': 85, 'master': 85,
            'mba': 85, 'bachelors': 70, 'bachelor': 70, 'b.tech': 70,
            'b.e': 70, 'associate': 50, 'diploma': 40, 'high school': 30,
            'mbbs': 90, 'md': 90, 'llb': 80, 'ca': 85, 'b.com': 65,
            'm.com': 75, 'b.ed': 70, 'm.ed': 80, 'b.sc': 65, 'm.sc': 75
        }
        
        text_lower = text.lower()
        max_score = 0
        
        for keyword, score in education_keywords.items():
            if keyword in text_lower:
                max_score = max(max_score, score)
        
        return max_score if max_score > 0 else 20
    
    def calculate_formatting_score(self, text: str) -> float:
        score = 0
        word_count = len(text.split())
        
        if 300 <= word_count <= 1000:
            score += 30
        elif 200 <= word_count <= 1200:
            score += 20
        else:
            score += 10
        
        if re.search(r'(?i)experience', text):
            score += 20
        if re.search(r'(?i)education', text):
            score += 20
        if re.search(r'(?i)skills', text):
            score += 15
        
        if re.search(r'[\w\.-]+@[\w\.-]+', text):
            score += 15
        
        return min(score, 100)
    
    def calculate_keyword_score(self, text: str) -> float:
        action_verbs = [
            'developed', 'created', 'managed', 'led', 'implemented',
            'designed', 'improved', 'increased', 'reduced', 'achieved',
            'launched', 'built', 'optimized', 'automated', 'collaborated'
        ]
        
        text_lower = text.lower()
        found_verbs = [verb for verb in action_verbs if verb in text_lower]
        percentage = (len(found_verbs) / len(action_verbs)) * 100
        
        return percentage
    
    def get_grade(self, score: float) -> str:
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B+'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C'
        else:
            return 'D'
    
    def predict_career_roles(self, resume_text: str, extracted_skills: Dict) -> List[Dict]:
        """Predict career roles based on resume content"""
        all_resume_skills = []
        for category, skills in extracted_skills.items():
            if isinstance(skills, list):
                all_resume_skills.extend([s.lower() for s in skills])
        
        resume_text_lower = resume_text.lower()
        career_predictions = []
        
        for role, requirements in self.career_database.items():
            required_skills_lower = [s.lower() for s in requirements["skills"]]
            matching_skills = [s for s in required_skills_lower if s in all_resume_skills or s in resume_text_lower]
            skill_percentage = (len(matching_skills) / len(required_skills_lower)) * 100 if required_skills_lower else 0
            
            matching_keywords = [k for k in requirements["keywords"] if k.lower() in resume_text_lower]
            keyword_percentage = (len(matching_keywords) / len(requirements["keywords"])) * 100 if requirements["keywords"] else 0
            
            matching_education = [e for e in requirements["education"] if e.lower() in resume_text_lower]
            education_percentage = (len(matching_education) / len(requirements["education"])) * 100 if requirements["education"] else 0
            
            overall_match = round((skill_percentage * 0.5) + (keyword_percentage * 0.3) + (education_percentage * 0.2), 1)
            
            if overall_match > 15:
                career_predictions.append({
                    "role": role,
                    "match_percentage": overall_match,
                    "matching_skills": matching_skills[:5],
                    "skill_count": len(matching_skills),
                    "total_required_skills": len(required_skills_lower)
                })
        
        career_predictions.sort(key=lambda x: x["match_percentage"], reverse=True)
        return career_predictions[:10]
    
    def calculate_target_role_match(self, resume_text: str, extracted_skills: Dict, target_role: str) -> Dict:
        """Calculate match percentage for specific target role"""
        
        # Normalize target role
        target_role_lower = target_role.lower().strip()
        
        # Check role mapping
        if target_role_lower in self.role_mapping:
            target_role = self.role_mapping[target_role_lower]
        elif target_role in self.career_database:
            pass  # Exact match
        else:
            # Try to find partial match
            for role in self.career_database:
                if target_role_lower in role.lower() or role.lower() in target_role_lower:
                    target_role = role
                    break
        
        if target_role not in self.career_database:
            return {
                'target_role': target_role,
                'match_percentage': 0,
                'advice': 'This profession is not in our database yet. We will add it soon!',
                'matching_skills': [],
                'missing_skills': [],
                'required_skills': [],
                'matching_keywords': [],
                'education_match': []
            }
        
        requirements = self.career_database[target_role]
        
        # Collect resume skills
        all_resume_skills = []
        for category, skills in extracted_skills.items():
            if isinstance(skills, list):
                all_resume_skills.extend([s.lower().strip() for s in skills])
        
        resume_text_lower = resume_text.lower()
        
        # Match skills
        required_skills = requirements.get("skills", [])
        matching_skills = []
        missing_skills = []
        
        for skill in required_skills:
            skill_lower = skill.lower().strip()
            # Check in extracted skills OR in resume text
            if skill_lower in all_resume_skills or skill_lower in resume_text_lower:
                matching_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        skill_percentage = (len(matching_skills) / len(required_skills)) * 100 if required_skills else 0
        
        # Match keywords
        keywords = requirements.get("keywords", [])
        matching_keywords = [k for k in keywords if k.lower() in resume_text_lower]
        keyword_percentage = (len(matching_keywords) / len(keywords)) * 100 if keywords else 0
        
        # Match education
        education = requirements.get("education", [])
        matching_education = [e for e in education if e.lower() in resume_text_lower]
        education_percentage = (len(matching_education) / len(education)) * 100 if education else 0
        
        # Overall match
        overall_match = round((skill_percentage * 0.5) + (keyword_percentage * 0.3) + (education_percentage * 0.2), 1)
        
        # Advice
        if overall_match >= 75:
            advice = "Excellent match! You have strong potential for this career."
        elif overall_match >= 50:
            advice = "Good match! With some skill development, you can excel in this field."
        elif overall_match >= 30:
            advice = "Fair match. You need to develop more relevant skills."
        else:
            advice = "This career may not be the best fit. Consider exploring other options."
        
        return {
            'target_role': target_role,
            'match_percentage': overall_match,
            'advice': advice,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'required_skills': required_skills,
            'matching_keywords': matching_keywords,
            'education_match': matching_education
        }