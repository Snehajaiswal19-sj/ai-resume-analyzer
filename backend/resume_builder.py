from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
import os

class ResumeBuilder:
    """Build professional resume PDF with templates"""
    
    def generate_resume(self, data: dict, output_path: str) -> str:
        template = data.get('template', 'classic')
        
        doc = SimpleDocTemplate(output_path, pagesize=A4, 
                                leftMargin=15*mm, rightMargin=15*mm,
                                topMargin=15*mm, bottomMargin=15*mm)
        
        story = []
        
        # Generate based on template
        if template == 'gradient':
            story = self._build_gradient_template(data)
        elif template == 'minimal':
            story = self._build_minimal_template(data)
        elif template == 'corporate':
            story = self._build_corporate_template(data)
        elif template == 'dark':
            story = self._build_dark_template(data)
        elif template == 'creative':
            story = self._build_creative_template(data)
        elif template == 'elegant':
            story = self._build_elegant_template(data)
        elif template == 'bold':
            story = self._build_bold_template(data)
        elif template == 'nature':
            story = self._build_nature_template(data)
        elif template == 'golden':
            story = self._build_golden_template(data)
        elif template == 'ocean':
            story = self._build_ocean_template(data)
        elif template == 'royal':
            story = self._build_royal_template(data)
        else:
            story = self._build_classic_template(data)
        
        doc.build(story)
        return output_path
    
    def _build_classic_template(self, data):
        """Classic Professional - Black & White"""
        story = []
        styles = getSampleStyleSheet()
        
        # Name
        name_style = ParagraphStyle('Name', fontSize=24, alignment=TA_CENTER, 
                                    fontName='Helvetica-Bold', spaceAfter=5, textColor=colors.HexColor('#2c3e50'))
        story.append(Paragraph(data.get('name', '').upper(), name_style))
        
        # Contact
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        if data.get('location'):
            contact += f" | {data.get('location', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER, 
                                       textColor=colors.HexColor('#7f8c8d'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        # Line
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2c3e50')))
        story.append(Spacer(1, 15))
        
        # Summary
        if data.get('summary'):
            story.append(Paragraph("SUMMARY", self._section_style('#2c3e50')))
            story.append(Paragraph(data['summary'], self._body_style()))
            story.append(Spacer(1, 10))
        
        # Skills
        story.append(Paragraph("SKILLS", self._section_style('#2c3e50')))
        skills_text = data.get('technical_skills', '')
        if data.get('soft_skills'):
            skills_text += f" | {data['soft_skills']}"
        story.append(Paragraph(skills_text, self._body_style()))
        story.append(Spacer(1, 10))
        
        # Experience
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#2c3e50')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')} ({exp.get('duration', '')})"
                story.append(Paragraph(exp_text, self._body_style()))
                if exp.get('description'):
                    story.append(Paragraph(exp['description'], self._body_style()))
                story.append(Spacer(1, 8))
        
        # Education
        if data.get('educations'):
            story.append(Paragraph("EDUCATION", self._section_style('#2c3e50')))
            for edu in data['educations']:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')} ({edu.get('year', '')})"
                story.append(Paragraph(edu_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        # Projects
        if data.get('projects'):
            story.append(Paragraph("PROJECTS", self._section_style('#2c3e50')))
            for proj in data['projects']:
                proj_text = f"<b>{proj.get('name', '')}</b>"
                if proj.get('technologies'):
                    proj_text += f" - {proj['technologies']}"
                story.append(Paragraph(proj_text, self._body_style()))
                if proj.get('description'):
                    story.append(Paragraph(proj['description'], self._body_style()))
                story.append(Spacer(1, 8))
        
        return story
    
    def _build_gradient_template(self, data):
        """Modern Gradient - Purple theme"""
        story = []
        
        # Header with background color
        name_style = ParagraphStyle('Name', fontSize=24, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5, 
                                    textColor=colors.HexColor('#667eea'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#764ba2'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#667eea')))
        story.append(Spacer(1, 15))
        
        # Summary
        if data.get('summary'):
            story.append(Paragraph("SUMMARY", self._section_style('#667eea')))
            story.append(Paragraph(data['summary'], self._body_style()))
            story.append(Spacer(1, 10))
        
        # Skills
        story.append(Paragraph("SKILLS", self._section_style('#667eea')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        # Experience
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#667eea')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')} ({exp.get('duration', '')})"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        # Education
        if data.get('educations'):
            story.append(Paragraph("EDUCATION", self._section_style('#667eea')))
            for edu in data['educations']:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')}"
                story.append(Paragraph(edu_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_corporate_template(self, data):
        """Corporate Blue theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#1e3a5f'))
        story.append(Paragraph(data.get('name', '').upper(), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#64b5f6'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#1e3a5f')))
        story.append(Spacer(1, 15))
        
        if data.get('summary'):
            story.append(Paragraph("SUMMARY", self._section_style('#1e3a5f')))
            story.append(Paragraph(data['summary'], self._body_style()))
            story.append(Spacer(1, 10))
        
        story.append(Paragraph("SKILLS", self._section_style('#1e3a5f')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#1e3a5f')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')} ({exp.get('duration', '')})"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        if data.get('educations'):
            story.append(Paragraph("EDUCATION", self._section_style('#1e3a5f')))
            for edu in data['educations']:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')}"
                story.append(Paragraph(edu_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_minimal_template(self, data):
        """Minimalist - Green accent"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_LEFT,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#10b981'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, textColor=colors.HexColor('#6b7280'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#10b981')))
        story.append(Spacer(1, 15))
        
        if data.get('summary'):
            story.append(Paragraph(data['summary'], self._body_style()))
            story.append(Spacer(1, 10))
        
        story.append(Paragraph("SKILLS", self._section_style('#10b981')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#10b981')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_dark_template(self, data):
        """Dark theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#bb86fc'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#a0a0a0'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#bb86fc')))
        story.append(Spacer(1, 15))
        
        if data.get('summary'):
            story.append(Paragraph(data['summary'], self._body_style()))
            story.append(Spacer(1, 10))
        
        story.append(Paragraph("SKILLS", self._section_style('#bb86fc')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#bb86fc')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_creative_template(self, data):
        """Creative Pink theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#f5576c'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#f093fb'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#f5576c')))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("SKILLS", self._section_style('#f5576c')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('projects'):
            story.append(Paragraph("PROJECTS", self._section_style('#f5576c')))
            for proj in data['projects']:
                proj_text = f"<b>{proj.get('name', '')}</b>"
                story.append(Paragraph(proj_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_elegant_template(self, data):
        """Elegant Serif - Brown theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Times-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#5d4037'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#8d6e63'), spaceAfter=10,
                                       fontName='Times-Italic')
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#8b4513')))
        story.append(Spacer(1, 15))
        
        if data.get('summary'):
            story.append(Paragraph(data['summary'], self._body_style()))
            story.append(Spacer(1, 10))
        
        story.append(Paragraph("SKILLS", self._section_style('#5d4037')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#5d4037')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_bold_template(self, data):
        """Bold Red theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=24, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#c62828'))
        story.append(Paragraph(data.get('name', '').upper(), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#c62828'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#c62828')))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("SKILLS", self._section_style('#c62828')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#c62828')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_nature_template(self, data):
        """Nature Green theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#11998e'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#38ef7d'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#11998e')))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("SKILLS", self._section_style('#11998e')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('educations'):
            story.append(Paragraph("EDUCATION", self._section_style('#11998e')))
            for edu in data['educations']:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')}"
                story.append(Paragraph(edu_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_golden_template(self, data):
        """Golden Premium theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#ffd700'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#f0e68c'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#ffd700')))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("SKILLS", self._section_style('#ffd700')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#ffd700')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_ocean_template(self, data):
        """Ocean Blue theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#0072ff'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#00c6ff'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0072ff')))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("SKILLS", self._section_style('#0072ff')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('projects'):
            story.append(Paragraph("PROJECTS", self._section_style('#0072ff')))
            for proj in data['projects']:
                proj_text = f"<b>{proj.get('name', '')}</b> - {proj.get('technologies', '')}"
                story.append(Paragraph(proj_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _build_royal_template(self, data):
        """Purple Royal theme"""
        story = []
        
        name_style = ParagraphStyle('Name', fontSize=22, alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=5,
                                    textColor=colors.HexColor('#6a1b9a'))
        story.append(Paragraph(data.get('name', ''), name_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#ab47bc'), spaceAfter=10)
        story.append(Paragraph(contact, contact_style))
        
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#6a1b9a')))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("SKILLS", self._section_style('#6a1b9a')))
        story.append(Paragraph(data.get('technical_skills', ''), self._body_style()))
        story.append(Spacer(1, 10))
        
        if data.get('experiences'):
            story.append(Paragraph("EXPERIENCE", self._section_style('#6a1b9a')))
            for exp in data['experiences']:
                exp_text = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                story.append(Paragraph(exp_text, self._body_style()))
                story.append(Spacer(1, 5))
        
        return story
    
    def _section_style(self, color):
        return ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
                              textColor=colors.HexColor(color), spaceBefore=10, spaceAfter=5)
    
    def _body_style(self):
        return ParagraphStyle('Body', fontSize=10, fontName='Helvetica',
                              textColor=colors.HexColor('#333333'), spaceAfter=3)