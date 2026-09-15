import pdfplumber
import docx
import re
from typing import Dict, List, Optional
import os

class ResumeParser:
    """Parse resume files and extract text content"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text.strip()
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text based on file extension"""
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension == '.pdf':
            return ResumeParser.extract_text_from_pdf(file_path)
        elif extension == '.docx':
            return ResumeParser.extract_text_from_docx(file_path)
        elif extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract different sections from resume"""
        sections = {
            'education': '',
            'experience': '',
            'skills': '',
            'projects': '',
            'contact': ''
        }
        
        # Common section headers
        patterns = {
            'education': r'(?i)(education|academic|qualification)',
            'experience': r'(?i)(experience|employment|work history)',
            'skills': r'(?i)(skills|technical skills|competencies)',
            'projects': r'(?i)(projects|personal projects|academic projects)',
            'contact': r'(?i)(contact|personal information|details)'
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            for section, pattern in patterns.items():
                if re.search(pattern, line):
                    current_section = section
                    break
            
            if current_section:
                sections[current_section] += line + '\n'
        
        return sections
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {
            'email': '',
            'phone': '',
            'linkedin': '',
            'github': ''
        }
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone extraction
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
        
        # LinkedIn extraction
        linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9-]+'
        linkedin = re.findall(linkedin_pattern, text)
        if linkedin:
            contact_info['linkedin'] = linkedin[0]
        
        # GitHub extraction
        github_pattern = r'github\.com/[A-Za-z0-9-]+'
        github = re.findall(github_pattern, text)
        if github:
            contact_info['github'] = github[0]
        
        return contact_info