from typing import Dict, List
import re
import textstat

class AdvancedFeatures:
    """Additional resume analysis features"""
    
    def check_readability(self, text: str) -> Dict:
        """Calculate readability scores"""
        return {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'gunning_fog': textstat.gunning_fog(text),
            'smog_index': textstat.smog_index(text),
            'automated_readability_index': textstat.automated_readability_index(text),
            'reading_time_minutes': round(len(text.split()) / 200, 1)
        }
    
    def quantify_achievements(self, text: str) -> List[Dict]:
        """Detect quantitative achievements in resume"""
        patterns = [
            (r'(\d+)\s*%', 'percentage'),
            (r'(\d+)\s*(?:users|customers|clients)', 'users_impacted'),
            (r'\$\s*(\d+)', 'revenue_amount'),
            (r'(\d+)\s*(?:team|members|people)', 'team_size'),
            (r'(\d+)\s*(?:awards|patents|publications)', 'recognitions'),
            (r'(\d+)\s*(?:projects|applications|systems)', 'projects_delivered')
        ]
        
        achievements = []
        for pattern, category in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                achievements.append({
                    'category': category,
                    'count': len(matches),
                    'values': matches[:5]
                })
        
        return achievements
    
    def skill_gap_analysis(self, current_skills: List[str], target_role: str) -> Dict:
        """Analyze skill gaps for target role"""
        role_requirements = {
            "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "TensorFlow", "Deep Learning", "Data Visualization"],
            "Software Engineer": ["Java", "Python", "Git", "AWS", "Docker", "REST API", "Agile", "Unit Testing"],
            "Web Developer": ["JavaScript", "React", "Node.js", "HTML", "CSS", "TypeScript", "MongoDB", "Git"],
            "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD", "Terraform", "Python", "Monitoring"],
            "Business Analyst": ["SQL", "Excel", "Power BI", "Tableau", "Communication", "Requirements Gathering"],
            "UI/UX Designer": ["Figma", "Adobe XD", "Prototyping", "User Research", "HTML", "CSS", "Wireframing"],
            "Product Manager": ["Product Management", "Agile", "Data Analysis", "Communication", "Market Research", "Roadmapping"],
            "Chartered Accountant (CA)": ["Accounting", "Taxation", "Auditing", "Financial Reporting", "GST", "Tally", "Excel", "Compliance"],
            "Financial Analyst": ["Financial Analysis", "Excel", "Financial Modeling", "Valuation", "SQL", "Power BI", "Forecasting"],
            "Investment Banker": ["Financial Modeling", "Valuation", "M&A", "Excel", "PowerPoint", "Due Diligence"],
            "Marketing Manager": ["Digital Marketing", "SEO", "Social Media", "Content Strategy", "Google Analytics", "Brand Management"],
            "HR Manager": ["Recruitment", "Employee Relations", "HR Policies", "Performance Management", "Communication", "Payroll"],
            "Doctor": ["Patient Care", "Medical Diagnosis", "Treatment Planning", "Clinical Skills", "Medical Knowledge", "Communication"],
            "Nurse": ["Patient Care", "Medication Administration", "Clinical Skills", "Communication", "Emergency Care"],
            "Pharmacist": ["Pharmaceutical Knowledge", "Prescription Processing", "Patient Counseling", "Inventory Management"],
            "Lawyer": ["Legal Research", "Litigation", "Contract Law", "Legal Writing", "Negotiation", "Client Counseling"],
            "Civil Engineer": ["AutoCAD", "Structural Analysis", "Construction Management", "Surveying", "Project Planning"],
            "Mechanical Engineer": ["AutoCAD", "SolidWorks", "Thermodynamics", "Machine Design", "Manufacturing"],
            "Electrical Engineer": ["Circuit Design", "Power Systems", "PCB Design", "PLC", "Electrical Safety"],
            "Teacher": ["Teaching", "Lesson Planning", "Communication", "Classroom Management", "Curriculum Development"],
            "Professor": ["Teaching", "Research", "Academic Writing", "Mentoring", "Publication"],
            "Graphic Designer": ["Photoshop", "Illustrator", "InDesign", "Typography", "Branding", "Logo Design"],
            "Makeup Artist": ["Makeup Application", "Bridal Makeup", "Fashion Makeup", "Skin Care", "Color Theory"],
            "Photographer": ["Photography", "Photoshop", "Lightroom", "Lighting", "Composition"],
            "Content Writer": ["Writing", "SEO Writing", "Copywriting", "Content Strategy", "Editing"],
            "Video Editor": ["Premiere Pro", "After Effects", "Final Cut Pro", "Color Grading", "Motion Graphics"],
            "Chef": ["Cooking", "Menu Planning", "Food Safety", "Kitchen Management", "Recipe Development"],
            "Architect": ["AutoCAD", "3D Modeling", "Building Design", "SketchUp", "Construction Knowledge"],
            "Event Manager": ["Event Planning", "Vendor Management", "Budgeting", "Communication", "Coordination"],
            "Fashion Designer": ["Fashion Design", "Illustration", "Pattern Making", "Textile Knowledge", "Trend Analysis"],
            "Interior Designer": ["Interior Design", "AutoCAD", "3D Modeling", "Space Planning", "Color Theory"],
            "Sports Coach": ["Coaching", "Training", "Physical Fitness", "Motivation", "Team Management"],
            "Journalist": ["Writing", "Reporting", "Editing", "Research", "Communication", "Storytelling"],
            "Psychologist": ["Counseling", "Psychological Assessment", "Therapy", "Communication", "Research"],
            "Social Worker": ["Counseling", "Community Development", "Communication", "Case Management"],
            "Data Analyst": ["SQL", "Excel", "Python", "Tableau", "Power BI", "Data Visualization", "Statistics"],
            "Digital Marketer": ["SEO", "SEM", "Social Media Marketing", "Google Ads", "Content Marketing", "Email Marketing"],
            "Sales Manager": ["Sales", "Negotiation", "CRM", "Lead Generation", "Communication", "Team Management"],
            "Mobile App Developer": ["Android", "iOS", "Flutter", "React Native", "Kotlin", "Swift", "Java", "Firebase"],
            "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Computer Vision"],
            "Cloud Architect": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux", "Networking"],
            "Cybersecurity Analyst": ["Network Security", "Python", "Linux", "Firewall", "Penetration Testing", "SIEM", "Cryptography"]
        }
        
        if target_role not in role_requirements:
            return {
                'target_role': target_role,
                'required_skills': [],
                'matching_skills': [],
                'missing_skills': [],
                'gap_percentage': 0,
                'readiness': 0,
                'message': 'Role not found in database'
            }
        
        required = role_requirements[target_role]
        current_lower = [s.lower() for s in current_skills]
        
        matching = [s for s in required if s.lower() in current_lower]
        missing = [s for s in required if s.lower() not in current_lower]
        
        gap_percentage = (len(missing) / len(required)) * 100
        
        return {
            'target_role': target_role,
            'required_skills': required,
            'matching_skills': matching,
            'missing_skills': missing,
            'gap_percentage': round(gap_percentage, 1),
            'readiness': round(100 - gap_percentage, 1)
        }
    
    def suggest_certifications(self, skills: List[str], career_role: str) -> List[Dict]:
        """Suggest relevant certifications for any profession"""
        cert_database = {
            # Tech Roles
            "Data Scientist": [
                {"name": "Google Data Analytics Professional Certificate", "provider": "Google", "level": "Beginner", "link": "https://www.coursera.org/professional-certificates/google-data-analytics"},
                {"name": "AWS Certified Machine Learning", "provider": "AWS", "level": "Advanced", "link": "https://aws.amazon.com/certification/certified-machine-learning-specialty/"},
                {"name": "TensorFlow Developer Certificate", "provider": "Google", "level": "Intermediate", "link": "https://www.tensorflow.org/certificate"}
            ],
            "Software Engineer": [
                {"name": "AWS Certified Developer", "provider": "AWS", "level": "Intermediate", "link": "https://aws.amazon.com/certification/certified-developer-associate/"},
                {"name": "Oracle Certified Java Programmer", "provider": "Oracle", "level": "Intermediate", "link": "https://education.oracle.com/java-se-11-developer/pexam_1Z0-819"},
                {"name": "Microsoft Azure Developer", "provider": "Microsoft", "level": "Intermediate", "link": "https://learn.microsoft.com/en-us/certifications/azure-developer/"}
            ],
            "Web Developer": [
                {"name": "Meta Front-End Developer", "provider": "Meta", "level": "Beginner", "link": "https://www.coursera.org/professional-certificates/meta-front-end-developer"},
                {"name": "AWS Certified Solutions Architect", "provider": "AWS", "level": "Advanced", "link": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"}
            ],
            "DevOps Engineer": [
                {"name": "AWS Certified DevOps Engineer", "provider": "AWS", "level": "Advanced", "link": "https://aws.amazon.com/certification/certified-devops-engineer-professional/"},
                {"name": "Certified Kubernetes Administrator (CKA)", "provider": "CNCF", "level": "Advanced", "link": "https://www.cncf.io/certification/cka/"}
            ],
            "Cybersecurity Analyst": [
                {"name": "CompTIA Security+", "provider": "CompTIA", "level": "Beginner", "link": "https://www.comptia.org/certifications/security"},
                {"name": "CEH (Certified Ethical Hacker)", "provider": "EC-Council", "level": "Intermediate", "link": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/"}
            ],
            "Cloud Architect": [
                {"name": "AWS Certified Solutions Architect Professional", "provider": "AWS", "level": "Advanced", "link": "https://aws.amazon.com/certification/certified-solutions-architect-professional/"},
                {"name": "Google Cloud Architect", "provider": "Google", "level": "Advanced", "link": "https://cloud.google.com/certification/cloud-architect"}
            ],
            "Mobile App Developer": [
                {"name": "Google Associate Android Developer", "provider": "Google", "level": "Intermediate", "link": "https://developers.google.com/certification/associate-android-developer"},
                {"name": "Apple Certified iOS Developer", "provider": "Apple", "level": "Intermediate", "link": "https://training.apple.com/"}
            ],
            "AI Engineer": [
                {"name": "Deep Learning Specialization", "provider": "DeepLearning.AI", "level": "Intermediate", "link": "https://www.coursera.org/specializations/deep-learning"},
                {"name": "NVIDIA Deep Learning Certificate", "provider": "NVIDIA", "level": "Advanced", "link": "https://www.nvidia.com/en-us/training/"}
            ],
            
            # Business & Finance
            "Chartered Accountant (CA)": [
                {"name": "Chartered Accountancy (CA)", "provider": "ICAI", "level": "Professional", "link": "https://www.icai.org/"},
                {"name": "CPA (Certified Public Accountant)", "provider": "AICPA", "level": "Professional", "link": "https://www.aicpa.org/"},
                {"name": "ACCA (Association of Chartered Certified Accountants)", "provider": "ACCA", "level": "Professional", "link": "https://www.accaglobal.com/"}
            ],
            "Financial Analyst": [
                {"name": "CFA (Chartered Financial Analyst)", "provider": "CFA Institute", "level": "Advanced", "link": "https://www.cfainstitute.org/"},
                {"name": "Financial Modeling & Valuation Analyst (FMVA)", "provider": "CFI", "level": "Intermediate", "link": "https://corporatefinanceinstitute.com/certifications/fmva/"}
            ],
            "Investment Banker": [
                {"name": "CFA (Chartered Financial Analyst)", "provider": "CFA Institute", "level": "Advanced", "link": "https://www.cfainstitute.org/"},
                {"name": "Series 79 Investment Banking Exam", "provider": "FINRA", "level": "Professional", "link": "https://www.finra.org/"}
            ],
            "Business Analyst": [
                {"name": "CBAP (Certified Business Analysis Professional)", "provider": "IIBA", "level": "Advanced", "link": "https://www.iiba.org/business-analysis-certifications/cbap/"},
                {"name": "Google Data Analytics", "provider": "Google", "level": "Beginner", "link": "https://www.coursera.org/professional-certificates/google-data-analytics"}
            ],
            "Marketing Manager": [
                {"name": "Google Digital Marketing Certificate", "provider": "Google", "level": "Beginner", "link": "https://grow.google/certificates/digital-marketing/"},
                {"name": "HubSpot Content Marketing", "provider": "HubSpot", "level": "Intermediate", "link": "https://academy.hubspot.com/courses/content-marketing"}
            ],
            "HR Manager": [
                {"name": "SHRM-CP", "provider": "SHRM", "level": "Professional", "link": "https://www.shrm.org/certification/"},
                {"name": "PHR (Professional in Human Resources)", "provider": "HRCI", "level": "Professional", "link": "https://www.hrci.org/"}
            ],
            "Product Manager": [
                {"name": "Google Project Management Certificate", "provider": "Google", "level": "Beginner", "link": "https://www.coursera.org/professional-certificates/google-project-management"},
                {"name": "Certified Scrum Product Owner (CSPO)", "provider": "Scrum Alliance", "level": "Intermediate", "link": "https://www.scrumalliance.org/get-certified/product-owner-track/certified-scrum-product-owner"}
            ],
            "Sales Manager": [
                {"name": "Certified Sales Professional (CSP)", "provider": "NASP", "level": "Professional", "link": "https://www.nasp.com/"},
                {"name": "HubSpot Sales Software", "provider": "HubSpot", "level": "Beginner", "link": "https://academy.hubspot.com/courses/sales-software"}
            ],
            "Entrepreneur": [
                {"name": "Entrepreneurship Specialization", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/specializations/entrepreneurship"},
                {"name": "Business Strategy", "provider": "Harvard Business School", "level": "Advanced", "link": "https://online.hbs.edu/"}
            ],
            
            # Creative Roles
            "UI/UX Designer": [
                {"name": "Google UX Design Professional Certificate", "provider": "Google", "level": "Beginner", "link": "https://www.coursera.org/professional-certificates/google-ux-design"},
                {"name": "Adobe Certified Professional", "provider": "Adobe", "level": "Intermediate", "link": "https://learning.adobe.com/certification.html"}
            ],
            "Graphic Designer": [
                {"name": "Adobe Certified Professional in Visual Design", "provider": "Adobe", "level": "Intermediate", "link": "https://learning.adobe.com/certification.html"},
                {"name": "Graphic Design Specialization", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/specializations/graphic-design"}
            ],
            "Makeup Artist": [
                {"name": "Professional Makeup Artistry Certification", "provider": "QC Makeup Academy", "level": "Professional", "link": "https://www.qcmakeupacademy.com/"},
                {"name": "CIDESCO Beauty Therapy Diploma", "provider": "CIDESCO", "level": "Professional", "link": "https://www.cidesco.com/"}
            ],
            "Photographer": [
                {"name": "Professional Photography Certification", "provider": "PPA", "level": "Professional", "link": "https://www.ppa.com/"},
                {"name": "Adobe Photoshop Certification", "provider": "Adobe", "level": "Intermediate", "link": "https://learning.adobe.com/certification.html"}
            ],
            "Content Writer": [
                {"name": "HubSpot Content Marketing Certification", "provider": "HubSpot", "level": "Beginner", "link": "https://academy.hubspot.com/courses/content-marketing"},
                {"name": "Copywriting Mastery", "provider": "Udemy", "level": "Beginner", "link": "https://www.udemy.com/"}
            ],
            "Video Editor": [
                {"name": "Adobe Premiere Pro Certification", "provider": "Adobe", "level": "Intermediate", "link": "https://learning.adobe.com/certification.html"},
                {"name": "After Effects Certification", "provider": "Adobe", "level": "Intermediate", "link": "https://learning.adobe.com/certification.html"}
            ],
            "Fashion Designer": [
                {"name": "Fashion Design Certificate", "provider": "Parsons School of Design", "level": "Intermediate", "link": "https://www.newschool.edu/parsons/"},
                {"name": "Textile Design Certification", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/"}
            ],
            "Interior Designer": [
                {"name": "NCIDQ Certification", "provider": "CIDQ", "level": "Professional", "link": "https://www.cidq.org/"},
                {"name": "Interior Design Certificate", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/"}
            ],
            
            # Medical
            "Doctor": [
                {"name": "USMLE", "provider": "USMLE", "level": "Professional", "link": "https://www.usmle.org/"},
                {"name": "MRCP", "provider": "RCP", "level": "Advanced", "link": "https://www.mrcpuk.org/"}
            ],
            "Nurse": [
                {"name": "NCLEX-RN", "provider": "NCSBN", "level": "Professional", "link": "https://www.ncsbn.org/nclex.htm"},
                {"name": "BLS/ACLS Certification", "provider": "AHA", "level": "Essential", "link": "https://cpr.heart.org/"}
            ],
            "Pharmacist": [
                {"name": "NAPLEX", "provider": "NABP", "level": "Professional", "link": "https://nabp.pharmacy/programs/naplex/"},
                {"name": "PTCB Certification", "provider": "PTCB", "level": "Professional", "link": "https://www.ptcb.org/"}
            ],
            
            # Legal
            "Lawyer": [
                {"name": "Bar Council License", "provider": "Bar Council of India", "level": "Professional", "link": "http://www.barcouncilofindia.org/"},
                {"name": "LLM Specialization", "provider": "Various Universities", "level": "Advanced", "link": "https://www.law.cornell.edu/"}
            ],
            
            # Engineering
            "Civil Engineer": [
                {"name": "PE (Professional Engineer) License", "provider": "NCEES", "level": "Professional", "link": "https://ncees.org/"},
                {"name": "LEED Certification", "provider": "USGBC", "level": "Intermediate", "link": "https://www.usgbc.org/leed"}
            ],
            "Mechanical Engineer": [
                {"name": "PE (Professional Engineer) License", "provider": "NCEES", "level": "Professional", "link": "https://ncees.org/"},
                {"name": "SolidWorks Certification", "provider": "Dassault Systèmes", "level": "Intermediate", "link": "https://www.solidworks.com/certification"}
            ],
            "Electrical Engineer": [
                {"name": "PE (Professional Engineer) License", "provider": "NCEES", "level": "Professional", "link": "https://ncees.org/"},
                {"name": "IPC Certification", "provider": "IPC", "level": "Intermediate", "link": "https://www.ipc.org/"}
            ],
            
            # Education
            "Teacher": [
                {"name": "B.Ed (Bachelor of Education)", "provider": "Various Universities", "level": "Professional", "link": "https://www.ncte.gov.in/"},
                {"name": "TEFL/TESOL Certification", "provider": "TEFL", "level": "Intermediate", "link": "https://www.tefl.org/"}
            ],
            "Professor": [
                {"name": "UGC NET", "provider": "NTA", "level": "Professional", "link": "https://ugcnet.nta.nic.in/"},
                {"name": "PhD", "provider": "Various Universities", "level": "Advanced", "link": "https://www.ugc.ac.in/"}
            ],
            
            # Other Professions
            "Chef": [
                {"name": "Culinary Arts Certification", "provider": "Culinary Institute of America", "level": "Professional", "link": "https://www.ciachef.edu/"},
                {"name": "Food Safety Certification", "provider": "ServSafe", "level": "Essential", "link": "https://www.servsafe.com/"}
            ],
            "Architect": [
                {"name": "Architect License", "provider": "Council of Architecture", "level": "Professional", "link": "https://www.coa.gov.in/"},
                {"name": "LEED AP", "provider": "USGBC", "level": "Advanced", "link": "https://www.usgbc.org/leed"}
            ],
            "Event Manager": [
                {"name": "CMP (Certified Meeting Professional)", "provider": "Events Industry Council", "level": "Professional", "link": "https://www.eventscouncil.org/"},
                {"name": "Event Planning Certificate", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/"}
            ],
            "Sports Coach": [
                {"name": "Certified Personal Trainer", "provider": "ACE", "level": "Professional", "link": "https://www.acefitness.org/"},
                {"name": "Sports Coaching Certificate", "provider": "National Sports Federations", "level": "Intermediate", "link": "https://www.nsnis.org/"}
            ],
            "Journalist": [
                {"name": "Journalism Certificate", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/"},
                {"name": "Digital Journalism", "provider": "Reuters", "level": "Intermediate", "link": "https://reutersdigitaljournalism.com/"}
            ],
            "Psychologist": [
                {"name": "RCI Registration", "provider": "Rehabilitation Council of India", "level": "Professional", "link": "http://www.rehabcouncil.nic.in/"},
                {"name": "Clinical Psychology Certification", "provider": "Various Universities", "level": "Advanced", "link": "https://www.apa.org/"}
            ],
            "Social Worker": [
                {"name": "MSW (Master of Social Work)", "provider": "Various Universities", "level": "Professional", "link": "https://www.ugc.ac.in/"},
                {"name": "Social Work Certificate", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/"}
            ],
            "Data Analyst": [
                {"name": "Google Data Analytics", "provider": "Google", "level": "Beginner", "link": "https://www.coursera.org/professional-certificates/google-data-analytics"},
                {"name": "Microsoft Power BI Certification", "provider": "Microsoft", "level": "Intermediate", "link": "https://learn.microsoft.com/en-us/certifications/power-bi/"}
            ],
            "Digital Marketer": [
                {"name": "Google Digital Marketing", "provider": "Google", "level": "Beginner", "link": "https://grow.google/certificates/digital-marketing/"},
                {"name": "HubSpot Inbound Marketing", "provider": "HubSpot", "level": "Beginner", "link": "https://academy.hubspot.com/courses/inbound-marketing"}
            ],
            
            # Default
            "default": [
                {"name": "Professional Development Certificate", "provider": "LinkedIn Learning", "level": "Beginner", "link": "https://www.linkedin.com/learning/"},
                {"name": "Industry-Specific Certification", "provider": "Professional Bodies", "level": "Intermediate", "link": "https://www.coursera.org/"},
                {"name": "Communication and Leadership", "provider": "Coursera", "level": "Beginner", "link": "https://www.coursera.org/"}
            ]
        }
        
        if career_role in cert_database:
            return cert_database[career_role]
        else:
            return cert_database["default"]
    
    def industry_analysis(self, text: str, skills: List[str], industry: str) -> Dict:
        """Industry-specific analysis"""
        industries = {
            'IT': {
                'keywords': ['software', 'coding', 'database', 'cloud', 'API'],
                'description': 'Information Technology'
            },
            'Finance': {
                'keywords': ['financial', 'banking', 'investment', 'risk', 'analysis'],
                'description': 'Finance & Banking'
            },
            'Marketing': {
                'keywords': ['marketing', 'SEO', 'social media', 'campaign', 'brand'],
                'description': 'Marketing & Advertising'
            },
            'Healthcare': {
                'keywords': ['health', 'medical', 'patient', 'clinical', 'care'],
                'description': 'Healthcare & Medical'
            }
        }
        
        if industry not in industries:
            return {'error': 'Industry not found'}
        
        config = industries[industry]
        text_lower = text.lower()
        matching_keywords = [k for k in config['keywords'] if k in text_lower]
        keyword_score = len(matching_keywords) / len(config['keywords']) * 100
        
        return {
            'industry': industry,
            'description': config['description'],
            'keyword_score': round(keyword_score, 2),
            'matching_keywords': matching_keywords,
            'missing_keywords': [k for k in config['keywords'] if k not in text_lower]
        }
    
    def check_grammar(self, text: str) -> Dict:
        """Check grammar errors"""
        try:
            import language_tool_python
            tool = language_tool_python.LanguageTool('en-US')
            matches = tool.check(text)
            
            errors = []
            for match in matches[:10]:
                errors.append({
                    'message': match.message,
                    'context': match.context,
                    'suggestions': match.replacements[:3]
                })
            
            return {
                'total_errors': len(matches),
                'errors': errors
            }
        except Exception as e:
            return {'error': str(e)}