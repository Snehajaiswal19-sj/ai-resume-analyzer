from typing import Dict

class CoverLetterGenerator:
    """Generate personalized cover letter based on resume"""
    
    def __init__(self):
        self.templates = {
            'software_engineer': """
Dear Hiring Manager,

I am writing to express my strong interest in the Software Engineer position at your company. With {experience} years of experience and expertise in {skills}, I am confident in my ability to contribute to your team.

Throughout my career, I have developed strong skills in {primary_skills}. My experience includes working on projects involving {projects}, where I successfully delivered high-quality solutions.

Some highlights of my qualifications include:
• Proficient in {skills_list}
• {achievement}
• Strong problem-solving and analytical skills

I am particularly excited about the opportunity to work with your team because of your company's innovative approach to technology. I am eager to bring my expertise in {primary_skills} to help drive success.

Thank you for considering my application. I look forward to discussing how I can contribute to your team.

Best regards,
{name}
""",
            'data_scientist': """
Dear Hiring Manager,

I am excited to apply for the Data Scientist position. With a strong background in {primary_skills} and hands-on experience in data analysis, I am well-prepared to contribute to your data-driven initiatives.

Key qualifications:
• Advanced proficiency in {skills_list}
• Experience with statistical analysis and machine learning
• Proven track record of {achievement}

I am passionate about leveraging data to solve complex business problems and would welcome the opportunity to discuss how my skills align with your team's goals.

Thank you for your consideration.

Best regards,
{name}
"""
        }
    
    def generate_cover_letter(self, resume_text: str, extracted_skills: Dict, job_role: str = None) -> str:
        """Generate personalized cover letter"""
        
        # Extract name (first line usually)
        lines = resume_text.strip().split('\n')
        name = lines[0].strip() if lines else "Candidate"
        
        # Extract experience
        import re
        experience_match = re.search(r'(\d+)\s*years?', resume_text)
        experience = experience_match.group(1) if experience_match else "relevant"
        
        # Get skills
        all_skills = []
        for category, skills in extracted_skills.items():
            all_skills.extend(skills)
        
        primary_skills = ', '.join(all_skills[:3]) if all_skills else "relevant technologies"
        skills_list = ', '.join(all_skills[:8]) if all_skills else "relevant skills"
        
        # Determine template
        if job_role and 'data' in job_role.lower():
            template = self.templates['data_scientist']
        else:
            template = self.templates['software_engineer']
        
        # Fill template
        cover_letter = template.format(
            name=name,
            experience=experience,
            skills=skills_list,
            primary_skills=primary_skills,
            skills_list=skills_list,
            achievement="Delivered high-impact projects that improved efficiency and performance",
            projects="scalable applications and data-driven solutions"
        )
        
        return cover_letter