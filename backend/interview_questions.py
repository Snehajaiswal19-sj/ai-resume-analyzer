from typing import List, Dict
import random

class InterviewQuestionGenerator:
    """Generate personalized interview questions for any profession"""
    
    def __init__(self):
        self.technical_questions = {
            # Tech Roles
            "Python": [
                "Explain the difference between list and tuple",
                "What are decorators and how do they work?",
                "Explain GIL (Global Interpreter Lock)",
                "How does memory management work in Python?",
                "What are generators and when to use them?"
            ],
            "Java": [
                "Explain OOP principles with examples",
                "Difference between HashMap and ConcurrentHashMap",
                "How does JVM work?",
                "Explain multithreading and synchronization",
                "What are Java 8 streams?"
            ],
            "SQL": [
                "Write a query to find nth highest salary",
                "Explain different types of JOINs",
                "What is indexing and how to optimize?",
                "Difference between WHERE and HAVING",
                "Explain ACID properties"
            ],
            "Machine Learning": [
                "Explain bias-variance tradeoff",
                "What is cross-validation?",
                "How to handle imbalanced datasets?",
                "Difference between L1 and L2 regularization",
                "Explain gradient descent"
            ],
            "Docker": [
                "Docker vs Virtual Machine",
                "How to reduce Docker image size?",
                "Explain Docker networking",
                "What is Docker Compose?"
            ],
            "AWS": [
                "Explain S3 storage classes",
                "What is VPC and how to secure it?",
                "Difference between RDS and DynamoDB",
                "How does Lambda work?"
            ],
            # Business & Finance
            "Accounting": [
                "What is the difference between accrual and cash accounting?",
                "Explain the accounting equation",
                "What are the three financial statements?",
                "How do you handle depreciation?",
                "What is working capital management?"
            ],
            "Taxation": [
                "Explain GST and its types",
                "What is the difference between direct and indirect tax?",
                "How is income tax calculated?",
                "What are tax deductions available?"
            ],
            "Auditing": [
                "What is the difference between internal and external audit?",
                "Explain audit planning process",
                "What are audit assertions?",
                "How to detect fraud during audit?"
            ],
            "Finance": [
                "Explain time value of money",
                "What is NPV and IRR?",
                "Difference between equity and debt financing",
                "Explain working capital cycle"
            ],
            # Creative Roles
            "Design": [
                "What is your design process?",
                "How do you handle client feedback?",
                "Explain the difference between UI and UX",
                "What design tools are you proficient in?"
            ],
            "Photography": [
                "Explain the exposure triangle",
                "What is the rule of thirds?",
                "How do you handle difficult lighting conditions?",
                "What's your post-processing workflow?"
            ],
            "Writing": [
                "How do you research for your articles?",
                "What's your writing process?",
                "How do you optimize content for SEO?",
                "How do you handle writer's block?"
            ],
            # Medical
            "Patient Care": [
                "How do you handle difficult patients?",
                "Explain your approach to patient assessment",
                "How do you prioritize patient care?",
                "What would you do in a medical emergency?"
            ],
            "Medical": [
                "How do you stay updated with medical advancements?",
                "Explain your diagnostic approach",
                "How do you handle medical errors?",
                "What's your experience with electronic health records?"
            ],
            # Legal
            "Legal": [
                "Explain the difference between civil and criminal law",
                "How do you prepare for a case?",
                "What's your approach to legal research?",
                "How do you handle difficult clients?"
            ],
            # General Professional
            "Communication": [
                "Describe a time you had to explain something complex",
                "How do you handle misunderstandings?",
                "Give an example of effective teamwork",
                "How do you handle negative feedback?"
            ],
            "Leadership": [
                "Describe your leadership style",
                "How do you motivate team members?",
                "Give an example of a difficult decision you made",
                "How do you handle underperforming team members?"
            ],
            "Management": [
                "How do you prioritize tasks?",
                "Describe a project you managed successfully",
                "How do you handle tight deadlines?",
                "What's your approach to resource allocation?"
            ],
            "Sales": [
                "How do you handle rejection?",
                "Describe your sales process",
                "How do you build client relationships?",
                "What's your approach to meeting targets?"
            ],
            "Teaching": [
                "How do you handle difficult students?",
                "What's your teaching philosophy?",
                "How do you make lessons engaging?",
                "How do you assess student progress?"
            ]
        }
        
        self.hr_questions = [
            "Tell me about yourself",
            "Why do you want to join our company?",
            "Where do you see yourself in 5 years?",
            "What are your strengths and weaknesses?",
            "Describe a challenging project and how you handled it",
            "How do you handle conflicts in a team?",
            "Why should we hire you?",
            "What motivates you?",
            "Describe a time you failed and what you learned",
            "How do you handle stress and pressure?"
        ]
        
        self.tips = [
            "Research the company before the interview",
            "Prepare examples using the STAR method (Situation, Task, Action, Result)",
            "Dress professionally and join 5 minutes early",
            "Prepare questions to ask the interviewer",
            "Review your resume thoroughly before interview",
            "Practice common interview questions",
            "Follow up with a thank-you email after interview",
            "Prepare a portfolio of your work if applicable"
        ]
    
    def generate_questions(self, skills: List[str], experience_years: int = 0) -> Dict:
        """Generate questions based on skills"""
        technical_qs = []
        
        # Match skills to questions
        for skill in skills[:8]:
            if skill in self.technical_questions:
                questions = self.technical_questions[skill]
                selected = random.sample(questions, min(2, len(questions)))
                technical_qs.extend(selected)
        
        # If no specific skill questions found, add general questions
        if not technical_qs:
            general_skills = ["Communication", "Leadership", "Management"]
            for skill in general_skills:
                if skill in self.technical_questions:
                    technical_qs.extend(self.technical_questions[skill][:2])
        
        # Limit to 6 technical questions
        technical_qs = technical_qs[:6]
        
        # Select HR questions based on experience
        if experience_years < 2:
            hr_qs = random.sample(self.hr_questions[:5], 3)
        elif experience_years < 5:
            hr_qs = random.sample(self.hr_questions[2:7], 3)
        else:
            hr_qs = random.sample(self.hr_questions[3:8], 3)
        
        # Random tips
        selected_tips = random.sample(self.tips, 3)
        
        return {
            'technical_questions': technical_qs,
            'hr_questions': hr_qs,
            'preparation_tips': selected_tips,
            'difficulty_level': 'Entry' if experience_years < 2 else 'Mid' if experience_years < 5 else 'Senior'
        }