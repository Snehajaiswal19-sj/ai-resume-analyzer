from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from typing import Dict
import os

class PDFGenerator:
    """Generate professional PDF report"""
    
    def generate_report(self, analysis_result: Dict, output_path: str) -> str:
        """Generate PDF report from analysis results"""
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30
        )
        story.append(Paragraph("AI Resume Analyzer Report", title_style))
        story.append(Spacer(1, 20))
        
        # Overall Score
        score_text = f"""
        <font size="14"><b>Overall Score: {analysis_result['scores']['total_score']}%</b></font><br/>
        <font size="12">Grade: {analysis_result['scores']['grade']}</font>
        """
        story.append(Paragraph(score_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Score Breakdown Table
        data = [
            ['Category', 'Score'],
            ['Skills', f"{analysis_result['scores']['skills_score']}%"],
            ['Experience', f"{analysis_result['scores']['experience_score']}%"],
            ['Education', f"{analysis_result['scores']['education_score']}%"],
            ['Formatting', f"{analysis_result['scores']['formatting_score']}%"],
            ['Keywords', f"{analysis_result['scores']['keyword_score']}%"]
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Skills Section
        story.append(Paragraph("Extracted Skills", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        skills_text = f"""
        <b>Technical Skills:</b> {', '.join(analysis_result['extracted_skills']['technical_skills'])}<br/><br/>
        <b>Soft Skills:</b> {', '.join(analysis_result['extracted_skills']['soft_skills'])}<br/><br/>
        <b>Domain Skills:</b> {', '.join(analysis_result['extracted_skills']['domain_skills'])}
        """
        story.append(Paragraph(skills_text, styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Career Predictions
        if analysis_result.get('career_predictions'):
            story.append(Paragraph("Career Predictions", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            career_data = [['Role', 'Match %']]
            for career in analysis_result['career_predictions']:
                career_data.append([career['role'], f"{career['match_percentage']}%"])
            
            career_table = Table(career_data)
            career_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(career_table)
        
        # Build PDF
        doc.build(story)
        
        return output_path