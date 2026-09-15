import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

class EmailSender:
    """Send reports via email using .env configuration"""
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('EMAIL_USER', '')
        self.sender_password = os.getenv('EMAIL_PASSWORD', '')
        
        if not self.sender_email or not self.sender_password:
            print("⚠️ Email credentials not found in .env file!")
            print("Please add EMAIL_USER and EMAIL_PASSWORD to .env")
    
    def send_analysis_report(self, to_email: str, analysis_result: Dict, pdf_path: str = None) -> Dict:
        """Send analysis report email"""
        try:
            if not self.sender_email or not self.sender_password:
                return {
                    'success': False,
                    'error': 'Email credentials not configured. Please check .env file.'
                }
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = f"Your Resume Analysis Report - Score: {analysis_result.get('scores', {}).get('total_score', 'N/A')}%"
            
            # HTML body
            body = self._create_email_body(analysis_result)
            msg.attach(MIMEText(body, 'html'))
            
            # Attach PDF if available
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='pdf')
                    attachment.add_header('Content-Disposition', 'attachment', filename='resume_report.pdf')
                    msg.attach(attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return {
                'success': True,
                'message': f'Report sent successfully to {to_email}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_email_body(self, result: Dict) -> str:
        """Create beautiful HTML email body"""
        scores = result.get('scores', {})
        career_predictions = result.get('career_predictions', [])
        extracted_skills = result.get('extracted_skills', {})
        
        # Get career predictions HTML
        career_html = ''
        for career in career_predictions[:3]:
            career_html += f"<li><strong>{career.get('role', 'N/A')}</strong>: {career.get('match_percentage', 0)}% match</li>"
        
        if not career_html:
            career_html = '<li>No career predictions available</li>'
        
        # Get skills
        technical_skills = ', '.join(extracted_skills.get('technical_skills', [])) or 'None'
        soft_skills = ', '.join(extracted_skills.get('soft_skills', [])) or 'None'
        domain_skills = ', '.join(extracted_skills.get('domain_skills', [])) or 'None'
        
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 30px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: auto; background: white; border-radius: 20px; padding: 30px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .score {{ font-size: 48px; color: #6366f1; font-weight: bold; }}
                .grade {{ font-size: 24px; color: #10b981; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f8fafc; border-radius: 10px; }}
                h2 {{ color: #4f46e5; font-size: 18px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 12px; }}
                ul {{ list-style: none; padding: 0; }}
                li {{ padding: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Resume Analysis Report</h1>
                    <div class="score">{scores.get('total_score', 'N/A')}%</div>
                    <div class="grade">Grade: {scores.get('grade', 'N/A')}</div>
                </div>
                
                <div class="section">
                    <h2>Score Breakdown</h2>
                    <ul>
                        <li>Skills: {scores.get('skills_score', 0)}%</li>
                        <li>Experience: {scores.get('experience_score', 0)}%</li>
                        <li>Education: {scores.get('education_score', 0)}%</li>
                        <li>Formatting: {scores.get('formatting_score', 0)}%</li>
                        <li>Keywords: {scores.get('keyword_score', 0)}%</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>Top Career Matches</h2>
                    <ul>
                        {career_html}
                    </ul>
                </div>
                
                <div class="section">
                    <h2>Skills Detected</h2>
                    <p><strong>Technical:</strong> {technical_skills}</p>
                    <p><strong>Soft Skills:</strong> {soft_skills}</p>
                    <p><strong>Domain:</strong> {domain_skills}</p>
                </div>
                
                <div class="footer">
                    <p>Generated by AI Resume Analyzer</p>
                    <p>Made with ❤️ using Python & Flask</p>
                </div>
            </div>
        </body>
        </html>
        """