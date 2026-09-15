from typing import List, Dict

class ResumeSuggestions:
    """Generate improvement suggestions"""
    
    @staticmethod
    def generate_suggestions(scores: Dict, extracted_skills: Dict, resume_text: str) -> List[Dict]:
        """Generate suggestions based on analysis"""
        suggestions = []
        
        # Skills suggestions
        if scores['skills_score'] < 70:
            suggestions.append({
                'category': 'Skills',
                'priority': 'High',
                'suggestion': 'Add more relevant technical skills to your resume',
                'impact': 'Improves keyword matching with job requirements'
            })
        
        # Experience suggestions
        if scores['experience_score'] < 60:
            suggestions.append({
                'category': 'Experience',
                'priority': 'High',
                'suggestion': 'Quantify your work experience with metrics and achievements',
                'impact': 'Shows tangible impact and results'
            })
        
        # Education suggestions
        if scores['education_score'] < 50:
            suggestions.append({
                'category': 'Education',
                'priority': 'Medium',
                'suggestion': 'Include relevant certifications and courses',
                'impact': 'Demonstrates continuous learning'
            })
        
        # Formatting suggestions
        if scores['formatting_score'] < 70:
            suggestions.append({
                'category': 'Formatting',
                'priority': 'Medium',
                'suggestion': 'Improve resume structure with clear sections',
                'impact': 'Better readability and ATS compatibility'
            })
        
        # Content suggestions
        if len(resume_text.split()) < 300:
            suggestions.append({
                'category': 'Content',
                'priority': 'High',
                'suggestion': 'Resume is too short. Add more details about your experience',
                'impact': 'Provides complete picture of your capabilities'
            })
        
        # Action verbs check
        action_verbs = ['developed', 'created', 'managed', 'led', 'implemented']
        found_verbs = [verb for verb in action_verbs if verb in resume_text.lower()]
        
        if len(found_verbs) < 3:
            suggestions.append({
                'category': 'Writing Style',
                'priority': 'Medium',
                'suggestion': 'Use more action verbs to start bullet points',
                'impact': 'Makes achievements more impactful'
            })
        
        return suggestions
    
    @staticmethod
    def generate_section_specific_suggestions(extracted_skills: Dict) -> Dict[str, List[str]]:
        """Generate section-specific suggestions"""
        section_suggestions = {}
        
        if len(extracted_skills.get('technical_skills', [])) < 5:
            section_suggestions['Technical Skills'] = [
                'Add programming languages',
                'Include frameworks and tools',
                'Mention cloud platforms'
            ]
        
        if len(extracted_skills.get('soft_skills', [])) < 3:
            section_suggestions['Soft Skills'] = [
                'Highlight leadership abilities',
                'Show communication skills',
                'Mention teamwork experiences'
            ]
        
        return section_suggestions