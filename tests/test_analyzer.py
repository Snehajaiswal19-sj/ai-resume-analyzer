import unittest
import os
import sys
from io import StringIO
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.resume_parser import ResumeParser
from backend.skill_extractor import SkillExtractor
from backend.score_calculator import ScoreCalculator
from backend.suggestions import ResumeSuggestions

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        # Create a sample text file for testing
        self.sample_text = """John Doe
Email: john@example.com
Phone: 123-456-7890
LinkedIn: linkedin.com/in/johndoe

Experience:
- Software Engineer at Tech Corp (2019-2023)
  Developed Python applications, worked with Django, React, AWS

Education:
- Bachelor of Technology in Computer Science

Skills:
Python, Java, SQL, Machine Learning, Docker, Kubernetes,
Communication, Leadership, Problem Solving"""
        
        # Write sample to temp file
        self.temp_file = 'test_resume.txt'
        with open(self.temp_file, 'w') as f:
            f.write(self.sample_text)
    
    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_extract_text_from_txt(self):
        text = self.parser.extract_text(self.temp_file)
        self.assertIn('John Doe', text)
        self.assertIn('Python', text)
    
    def test_extract_contact_info(self):
        contact = self.parser.extract_contact_info(self.sample_text)
        self.assertEqual(contact['email'], 'john@example.com')
        self.assertIn('123', contact['phone'])
        self.assertIn('linkedin.com/in/johndoe', contact['linkedin'])
    
    def test_extract_sections(self):
        sections = self.parser.extract_sections(self.sample_text)
        self.assertIn('Experience', sections['experience'])
        self.assertIn('Education', sections['education'])

class TestSkillExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = SkillExtractor()
    
    def test_extract_skills(self):
        text = "Proficient in Python, Java, Machine Learning, and Docker. Good communication and leadership skills."
        skills = self.extractor.extract_skills(text)
        self.assertIn('Python', skills['technical_skills'])
        self.assertIn('Communication', skills['soft_skills'])
    
    def test_missing_skills_suggestion(self):
        extracted = {'technical_skills': ['Python'], 'soft_skills': [], 'domain_skills': []}
        missing = self.extractor.suggest_missing_skills(extracted, 'data scientist')
        self.assertTrue(len(missing) > 0)

class TestScoreCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = ScoreCalculator()
    
    def test_total_score_range(self):
        text = "5 years experience as Software Engineer. Skills: Python, Java, AWS. Bachelor's degree. Developed many applications."
        skills = {'technical_skills': ['Python', 'Java', 'AWS'], 'soft_skills': [], 'domain_skills': []}
        scores = self.calculator.calculate_total_score(text, skills)
        self.assertGreaterEqual(scores['total_score'], 0)
        self.assertLessEqual(scores['total_score'], 100)
    
    def test_grade(self):
        self.assertEqual(self.calculator.get_grade(95), 'A+')
        self.assertEqual(self.calculator.get_grade(75), 'B+')

class TestSuggestions(unittest.TestCase):
    def test_generate_suggestions(self):
        scores = {'skills_score': 30, 'experience_score': 40, 'education_score': 20, 'formatting_score': 30}
        skills = {'technical_skills': [], 'soft_skills': [], 'domain_skills': []}
        suggestions = ResumeSuggestions.generate_suggestions(scores, skills, "short text")
        self.assertTrue(len(suggestions) > 0)

if __name__ == '__main__':
    unittest.main()